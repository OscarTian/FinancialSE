from django.db import models


# Create your models here.

class StockInfo(models.Model):
    # 所属股市
    stock_market = models.IntegerField(choices=((0, '深A'), (1, '沪A')), verbose_name='所属股市')
    code = models.CharField(max_length=10, verbose_name='股票代码')
    name = models.CharField(max_length=20, verbose_name='股票名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '股票信息'
        verbose_name_plural = verbose_name
