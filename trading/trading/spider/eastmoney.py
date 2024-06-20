import requests
import json


def get_stock_info(address, code):
    url = f'https://90.push2.eastmoney.com/api/qt/stock/sse?ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2&volt=2&fields=f152,f288,f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f116,f60,f45,f52,f50,f59,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f198,f259,f260,f261,f171,f277,f278,f279,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f20,f19,f18,f17,f16,f15,f14,f13,f12,f11,f531,f292,f301&secid={address}.{code}'
    with requests.get(url, stream=True) as response:
        if response.status_code != 200:
            return

        for line in response.iter_lines():
            # 过滤掉keep-alive新行
            if line:
                decoded_line = line.decode('utf-8').strip()
                if decoded_line.startswith("data:"):
                    data = decoded_line[len("data:"):]
                    data = json.loads(data)['data']

                    if not data:
                        return False
                    return dict(
                        # f43 当前价格
                        price=data['f43'],
                        # f58: 股票名称
                        name=data['f58'],
                        # f43: 最高
                        max=data['f44'],
                        # f45:最低
                        min=data['f45'],
                        # f46: 今开
                        today_price=data['f46'],
                        # f60: 昨收
                        last_day=data['f60'],
                        # 股票代码
                        code=data['f57']

                    )


# 获取股票5日数据
def get_stock_history(address, code):
    trend_history = []
    url = f'https://push2his.eastmoney.com/api/qt/stock/trends2/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58&ut=fa5fd1943c7b386f172d6893dbfba10b&secid={address}.{code}&ndays=5&iscr=0&iscca=0'
    response = requests.get(url)
    # {"rc":100,"rt":1,"svr":181669475,"lt":1,"full":1,"dlmkts":"","data":null}
    data = json.loads(response.text)['data']
    if not data:
        return False
    name = data['name']
    pre_price = data['prePrice']
    trends = data['trends']
    for trend in trends:
        # '2024-06-05 09:30,0.00,13.98,13.98,13.98,189,264222.00,13.980'
        d = trend.split(',')
        trend_history.append({'time': d[0], 'average': d[-1], 'price': d[2], 'turnover': d[-2], 'Volume': d[-3]})
    return trend_history


# 获取股票基本信息

if __name__ == '__main__':
    # print(get_stock_info(0, 301231))
    print(get_stock_info(0, 301231))
