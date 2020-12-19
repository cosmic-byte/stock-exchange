from django.contrib import admin

# Register your models here.
from stock_exchange.apps.company import models


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('user', 'ref_first_name', 'ref_last_name', 'company_name', 'company_symbol', 'date_added')
    search_fields = ('user__email', 'company_name', 'company_symbol')


admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.User)
