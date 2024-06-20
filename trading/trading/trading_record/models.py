from django.db import models


# Create your models here.
class TradingRecord(models.Model):
    # 所属股票
    stock = models.ForeignKey('stock.StockInfo', on_delete=models.CASCADE, verbose_name='股票')
    # 购买用户
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='购买用户')
    # 购买数量
    num = models.IntegerField(default=0, verbose_name='购买数量')
    # 单价
    price = models.FloatField(default=0, verbose_name='单价')
    # 购买时间
    buy_time = models.DateTimeField(auto_now_add=True, verbose_name='购买时间')
    # 总价
    total_price = models.FloatField(default=0, verbose_name='总价')
    # 状态,(持有,买出)
    status = models.IntegerField(choices=((0, '持有'), (1, '买出')), default=0, verbose_name='状态')

    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = verbose_name
