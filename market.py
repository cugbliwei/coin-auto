import requests


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4496.0 Safari/537.36'}
target_length = 7


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
        print('start to fetch url:' + link)
        resp = requests.get(link, headers=headers)
        rj = resp.json()
        return rj.get('data', [])
    except:
        return []


def predict(klines):
    if len(klines) != target_length:
        return False

    start_price = klines[0].get('open', 0)
    end_price = klines[-1].get('close', 0)
    target_rate = 0.1 * target_length
    if ((end_price - start_price) / start_price) > target_rate:
        return True
    '''
    for kline in klines:
        open_price = kline.get('open', 0)
        close_price = kline.get('close', 0)
        # low_price = kline.get('low', 0)
        # high_price = kline.get('high', 0)
        amount = kline.get('amount', 0)
    '''
    return False


def monitor():
    try:
        coins = get_all_coins()
        for coin_name in coins:
            klines = get_coin_kline(coin_name)
            if predict(klines):
                print(coin_name)
    except:
        pass


if __name__ == '__main__':
    get_all_coins()
