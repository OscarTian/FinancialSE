from django.contrib import admin
from wallet.models import Wallet


# Register your models here.
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    fieldsets = (
        (None, {'fields': ('balance', )}),
    )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            # 否则，仅显示当前用户创建的数据
            return qs.filter(user=request.user)
