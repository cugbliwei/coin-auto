import requests
import time
import json
import traceback
import mail


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4496.0 Safari/537.36'}
coin_filter = ['usdt', 'pundix', 'lsk', 'btg', 'salt', 'pay', 'powr', 'dgd', 'ven', 'qash', 'gas', 'eng', 'mco', 'mtl', 'rdn', 'chat', 'srn', 'qsp', 'req', 'phx', 'appc', 'rcn', 'adx', 'tnt', 'ost', 'lun', 'evx', 'snc', 'propy', 'eko', 'bcd', 'topc', 'dbc', 'aidoc', 'qun', 'dat', 'meet', 'bcx', 'sbtc', 'etf', 'bifi', 'zla', 'stk', 'wpr', 'mtn', 'mtx', 'edu', 'bft', 'wan', 'poly', 'box', 'dgb', 'xvg', 'ong', 'bt1', 'bt2', 'ncash', 'grs', 'egcc', 'she', 'mex', 'iic', 'gsc', 'uc', 'cnn', 'cdc', 'but', '18c', 'datx', 'portal', 'gtc', 'man', 'get', 'pc', 'eosdac', 'bkbt', 'gve', 'ycc', 'fair', 'ssp', 'eon', 'eop', 'lym', 'zjlt', 'meetone', 'pnt', 'idt', 'bcv', 'sexc', 'tos', 'musk', 'add', 'mt', 'iq', 'ncc', 'rccc', 'cvcoin', 'rte', 'trio', 'ardr', 'gusd', 'tusd', 'husd', 'rbtc', 'wgp', 'cova', 'cvnt', 'kmd', 'mgo', 'abl', 'mzk', 'etn', 'npxs', 'adt', 'mvl', 'hvt', 'tfuel', 'ugas', 'inc', 'pizza', 'eoss', 'usd01', 'nvt', 'lend', 'yamv2', 'bot', 'wbtc', 'renbtc', 'wing', 'bel', 'perp', 'rub', 'onx', 'gbp', 'kzt', 'uah', 'eur', 'bag', 'nsbt', 'don', 'xym', 'qi', 'btc3s', 'eth3s', 'link3s', 'bsv3s', 'bch3s', 'eos3s', 'ltc3s', 'xrp3s', 'zec3s', 'fil3s', 'btc3l', 'eth3l', 'link3l', 'bsv3l', 'bch3l', 'eos3l', 'ltc3l', 'xrp3l', 'zec3l', 'fil3l']
config = {}
max_times = 6


def get_config():
    global config
    with open('config.json', 'r') as f:
        config = json.load(f)


def write_json_to_file(rj):
    if not rj:
        return
    json_str = json.dumps(rj)
    with open('result.json', 'w') as f:
        f.write(json_str)


def get_host(is_default):
    if is_default:
        return 'api.huobi.pro'
    return'api-aws.huobi.pro'


def get_all_coins(times):
    try:
        link = 'https://%s/v1/common/currencys' % get_host(times % 2 == 0)
        resp = requests.get(link, headers=headers)
        rj = resp.json()
        coins = rj.get('data', [])
        if not coins and times < max_times:
            return get_all_coins(times + 1)
        return coins
    except:
        if times < max_times:
            return get_all_coins(times + 1)
        return []


def parse_time(klines):
    for i in range(0, len(klines)):
        # klines[i]['id'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(klines[i]['id']))
        klines[i]['id'] = time.strftime("%H:%M", time.localtime(klines[i]['id']))
    return klines


def get_coin_kline(coin_name, time_type, times):
    global config
    try:
        link = 'https://%s/market/history/kline?period=%s&size=%d&symbol=%susdt' % (get_host(times % 2 == 0), time_type, config['show_size'], coin_name)
        # print('start to fetch url:' + link)
        resp = requests.get(link, headers=headers)
        rj = resp.json()
        klines = rj.get('data', [])
        if not klines:
            if times < max_times:
                return get_coin_kline(coin_name, time_type, times + 1)
            print(link, rj)
            return True, []
        klines.reverse()
        klines = parse_time(klines)
        return True, klines
    except:
        if times < max_times:
            return get_coin_kline(coin_name, time_type, times + 1)
        return False, []


def predict(klines):
    global config
    if not klines or len(klines) < config['calculate_size']:
        return 0, 0, 0, False

    start_price = klines[len(klines) - config['calculate_size']].get('open', 0)
    end_price = klines[-1].get('close', 0)
    rate = (end_price - start_price) / start_price
    if rate > config['rate']:
        return rate, start_price, end_price, True
    return 0, 0, 0, False


def is_filter(coin_name):
    global config
    if coin_name in coin_filter:
        return True

    for filter_name in config['filter']:
        if coin_name.endswith(filter_name):
            return True
    return False


def monitor():
    try:
        # 获取最新配置信息
        get_config()
        global config

        predict_coins = []
        now_time = time.time()
        coins = get_all_coins(0)
        errors = 0
        rank = 1
        for coin_name in coins:
            if is_filter(coin_name):
                continue

            is_success, klines = get_coin_kline(coin_name, '1min', 0)
            errors += 1 if is_success else 0
            rate, start_price, end_price, is_predict = predict(klines)
            if is_predict:
                is_success, five_klines = get_coin_kline(coin_name, '5min', 0)
                if is_success:
                    obj = {
                        'key': coin_name,
                        'rank': rank,
                        'coin': coin_name,
                        'rate': '%.2f' % (rate * 100) + '%',
                        'start_price': start_price,
                        'end_price': end_price,
                        'one_minute_kline': klines,
                        'five_minute_kline': five_klines
                    }
                    rank += 1
                    predict_coins.append(obj)
            # api每秒最大为10，所以等待一下
            time.sleep(0.1)

        if len(predict_coins) == 0:
            if errors > 0 and config['email']:
                mail.send_mail('币种监测失败告警', "访问api链接失败")
            return

        end_time = time.time()
        cost_time = end_time - now_time
        # print('cost_time:', cost_time)
        if cost_time > 180:
            mail.send_mail('币种监测访问慢告警', "访问api链接访问慢")

        predict_coins = sorted(predict_coins, key=lambda i: i['rate'], reverse=True)
        write_json_to_file(predict_coins)
        # print(predict_coins)
        # msg = ''
        # for result in predict_coins:
        #     rate = '%.2f' % (result[1] * 100)
        #     coin_name = result[0]
        #     space = ' ' * (9 - len(coin_name))
        #     msg += result[0] + space + rate + '%' + '\n'
        # mail.send_mail('币种监测', msg)
    except:
        err = traceback.format_exc()
        print(err)
        mail.send_mail('币种监测执行错误', err)


if __name__ == '__main__':
    monitor()
