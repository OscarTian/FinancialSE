from django.contrib import admin
from django.utils.safestring import mark_safe

from stock.models import StockInfo
from spider.eastmoney import get_stock_info


# Register your models here.
@admin.register(StockInfo)
class StockInfoAdmin(admin.ModelAdmin):
    list_display = ('stock_market', 'code', 'name', 'show_config')
    fieldsets = (
        (None, {'fields': ('stock_market', 'code')}),
    )

    def show_config(self, obj):
        return mark_safe(
            '<a href="#" onclick="openIframeModal(\'/show_stock_info/{}\'); return false;">查看股票</a>'.format(obj.id))

    show_config.short_description = '股票数据'

    def save_model(self, request, obj, form, change):
        data = get_stock_info(obj.stock_market, obj.code)
        if not data:
            self.message_user(request, "当前股票不存在,请核对后输入")
            return False
        obj.name = data['name']
        super().save_model(request, obj, form, change)


admin.AdminSite.site_header = '量化交易系统'
admin.AdminSite.site_title = '量化交易系统'
