from django.shortcuts import render
from stock.models import StockInfo
from trading_record.models import TradingRecord
from wallet.models import Wallet
from django.contrib.auth.decorators import login_required
from spider.eastmoney import get_stock_info, get_stock_history
from django.db.models import Sum
from django.http import JsonResponse
from decimal import Decimal
import pandas as pd


# Create your views here.
@login_required
def show_stock_info(request, pk):
    stock_obj = StockInfo.objects.get(pk=pk)
    user = request.user
    wallet = Wallet.objects.get(user=user)

    record = TradingRecord.objects.filter(user=user, stock=stock_obj)

    # 我当前持有
    my_have = record.filter(status=0).aggregate(total=Sum('num'))['total']
    if request.method == 'POST':
        print(request.POST)
        # 获取股票价格
        # 进行买卖操作
        stock_info = get_stock_info(stock_obj.stock_market, stock_obj.code)
        price = stock_info['price']
        print(f'当前价格:{price}---{type(price)}')
        baynumber = request.POST.get('baynumber')
        sellnumber = request.POST.get('sellnumber')
        if baynumber:
            baynumber = int(baynumber)
            buy_price = price * baynumber
            if buy_price > wallet.balance:
                error = '余额不足!'
            else:
                wallet.balance -= buy_price
                TradingRecord.objects.create(
                    user=user,
                    stock=stock_obj,
                    num=baynumber,
                    price=price,
                    total_price=buy_price,
                    status=0,
                )
                wallet.save()
        if sellnumber:
            sellnumber = int(sellnumber)
            if sellnumber > my_have:
                error = '当前没有持有这么多股票'
            else:
                sell_price = price * sellnumber

                wallet.balance += sell_price
                TradingRecord.objects.create(
                    user=user,
                    stock=stock_obj,
                    num=sellnumber,
                    price=price,
                    total_price=sell_price,
                    status=1,
                )
                wallet.save()
    history_list = get_stock_history(stock_obj.stock_market, stock_obj.code)
    tips = quantification_tactics(history_list)
    return render(request, 'stockInfo.html', locals())


@login_required
def get_stock_data(request, pk):
    stock_obj = StockInfo.objects.get(pk=pk)
    # 股票基本信息
    stock_info = get_stock_info(stock_obj.stock_market, stock_obj.code)
    # 股票历史数据
    history_list = get_stock_history(stock_obj.stock_market, stock_obj.code)
    # {'time': d[0], 'average': d[-1], 'price': d[2], 'turnover': d[-2], 'Volume': d[-3]}
    x = []
    s = []
    for history in history_list:
        x.append(history['time'])
        s.append(history['price'])
    echarts_data = {
        "xAxis": {
            "type": "category",
            "data": x
        },
        "series": [
            {"name": "实时价格", "type": "line", "data": s},
        ]
    }

    return JsonResponse({'status': True, 'data': dict(stock_info=stock_info, echarts_data=echarts_data)})


# 量化交易的策略
def quantification_tactics(data):
    """
                    average  price      turnover Volume
time
2024-06-05 09:30:00  24.980  24.98   39445918.00  15791
2024-06-05 09:31:00  24.826  24.80  102523141.00  41394
2024-06-05 09:32:00  24.799  24.78   54027913.00  21848

    :param data:
    :return:
    """
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    last_three_hours = df[-3 * 60:]  # 假设每小时60分钟，共3小时

    # 按小时分组，取每小时的第一行和最后一行作为开始和结束价格
    hourly_start_end_prices = last_three_hours.groupby(last_three_hours.index.hour).agg({'price': ['first', 'last']})
    hourly_start_end_prices.columns = ['Start_Price', 'End_Price']
    # 取最后三组数据
    last_three_groups = hourly_start_end_prices.iloc[-3:]

    # 判断每组的'End_Price'是否大于'Start_Price'
    is_all_greater = (last_three_groups['End_Price'] > last_three_groups['Start_Price']).all()

    if is_all_greater:
        return "最近三小时中每小时的状态全部上涨,建议买入!"
    else:
        return "最近三小时中每小时的状态并非全部上涨,不建议买入!"
