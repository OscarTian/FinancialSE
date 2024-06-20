from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Wallet(models.Model):
    # 所属用户
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 可用余额
    balance = models.FloatField(default=1000)

    class Meta:
        verbose_name = '我的钱包'
        verbose_name_plural = verbose_name
