from django.contrib import admin

# Register your models here.
from stock_exchange.apps.stock import models


class StockAdmin(admin.ModelAdmin):
    list_display = ('company', 'open_amount_in_ngn', 'close_amount_in_usd', 'volume_amount_in_usd', 'data_time')
    search_fields = ('company__company_name', )


admin.site.register(models.Stock, StockAdmin)
