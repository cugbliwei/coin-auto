import requests
import time
import mail


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4496.0 Safari/537.36'}
target_length = 7
coin_filter = ['usdt', 'lsk', 'btg', 'salt', 'pay', 'powr', 'dgd', 'ven', 'qash', 'gas', 'eng', 'mco', 'mtl', 'rdn', 'chat', 'srn', 'qsp', 'req', 'phx', 'appc', 'rcn', 'adx', 'tnt', 'ost', 'lun', 'evx', 'snc', 'propy', 'eko', 'bcd', 'topc', 'dbc', 'aidoc', 'qun', 'dat', 'meet', 'bcx', 'sbtc', 'etf', 'bifi', 'zla', 'stk', 'wpr', 'mtn', 'mtx', 'edu', 'bft', 'wan', 'poly', 'box', 'dgb', 'xvg', 'ong', 'bt1', 'bt2', 'ncash', 'grs', 'egcc', 'she', 'mex', 'iic', 'gsc', 'uc', 'cnn', 'cdc', 'but', '18c', 'datx', 'portal', 'gtc', 'man', 'get', 'pc', 'eosdac', 'bkbt', 'gve', 'ycc', 'fair', 'ssp', 'eon', 'eop', 'lym', 'zjlt', 'meetone', 'pnt', 'idt', 'bcv', 'sexc', 'tos', 'musk', 'add', 'mt', 'iq', 'ncc', 'rccc', 'cvcoin', 'rte', 'trio', 'ardr', 'gusd', 'tusd', 'husd', 'rbtc', 'wgp', 'cova', 'cvnt', 'kmd', 'mgo', 'abl', 'mzk', 'etn', 'npxs', 'adt', 'mvl', 'hvt', 'tfuel', 'ugas', 'inc', 'pizza', 'eoss', 'usd01', 'nvt', 'lend', 'yamv2', 'bot', 'wbtc', 'renbtc', 'wing', 'bel', 'perp', 'rub', 'onx', 'gbp', 'kzt', 'uah', 'eur', 'bag', 'nsbt', 'don', 'xym', 'qi', 'btc3s', 'eth3s', 'link3s', 'bsv3s', 'bch3s', 'eos3s', 'ltc3s', 'xrp3s', 'zec3s', 'fil3s', 'btc3l', 'eth3l', 'link3l', 'bsv3l', 'bch3l', 'eos3l', 'ltc3l', 'xrp3l', 'zec3l', 'fil3l']


def get_all_coins():
    try:
        link = 'https://api.huobi.pro/v1/common/currencys'
        resp = requests.get(link, headers=headers)
        rj = resp.json()
        return rj.get('data', [])
    except:
        return []


def get_coin_kline(coin_name):
    try:
        link = 'https://api.huobi.pro/market/history/kline?period=1min&size=%d&symbol=%susdt' % (target_length, coin_name)
        # print('start to fetch url:' + link)
        resp = requests.get(link, headers=headers)
        rj = resp.json()
        '''
        if rj.get('status', '') != 'ok':
            print(coin_name)
        '''
        return rj.get('data', [])
    except:
        return []


def predict(klines):
    if not klines or len(klines) != target_length:
        return 0, False

    start_price = klines[-1].get('open', 0)
    end_price = klines[0].get('close', 0)
    # target_rate = 0.001 * target_length
    target_rate = 0.01
    rate = (end_price - start_price) / start_price
    if rate > target_rate:
        return rate, True
    '''
    for kline in klines:
        open_price = kline.get('open', 0)
        close_price = kline.get('close', 0)
        # low_price = kline.get('low', 0)
        # high_price = kline.get('high', 0)
        amount = kline.get('amount', 0)
    '''
    return 0, False


def monitor():
    try:
        predict_coins = {}
        now_time = time.time()
        coins = get_all_coins()
        for coin_name in coins:
            if coin_name in coin_filter or coin_name.endswith('3s') or coin_name.endswith('3l'):
                continue

            klines = get_coin_kline(coin_name)
            rate, is_target = predict(klines)
            if is_target:
                predict_coins[coin_name] = rate
            time.sleep(0.1)

        if len(predict_coins) == 0:
            return

        results = sorted(predict_coins.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        end_time = time.time()
        cost_time = end_time - now_time
        print(results)
        msg = ''
        for result in results:
            rate = '%.2f' % (result[1] * 100)
            coin_name = result[0]
            space = ' ' * (9 - len(coin_name))
            msg += result[0] + space + rate + '%' + '\n'
        mail.send_mail('币种监测', msg)
        # print('总共耗时：', cost_time)
    except:
        pass


if __name__ == '__main__':
    monitor()
