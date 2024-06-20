from django.contrib import admin
from trading_record.models import TradingRecord
# Register your models here.

@admin.register(TradingRecord)
class TradingRecordAdmin(admin.ModelAdmin):
    list_display = ('stock', 'user', 'num', 'price', 'buy_time', 'total_price', 'status')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # 如果用户是超级用户，则显示所有数据
            return qs
        else:
            # 否则，仅显示当前用户创建的数据
            return qs.filter(user=request.user)