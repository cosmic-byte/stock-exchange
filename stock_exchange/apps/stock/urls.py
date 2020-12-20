from django.conf.urls import url
from django.urls import path

from stock_exchange.apps.stock import views

app_name = 'stock'

urlpatterns = [
    url(r'^(?P<company_id>[0-9a-f-]+)/create/$', views.CreateStockDataView.as_view(), name='create_stock_data'),
    url(r'^(?P<pk>[0-9a-f-]+)/update/$', views.UpdateStockDataView.as_view(), name='update_stock_data'),
    url(r'^$', views.ListStockView.as_view(), name='list_company_stock'),
    url('^s_stock', views.SearchStockView.as_view({'get': 'list'}), name='stock_search'),
    path('<str:symbol>/<str:interval>', views.GetTimeSeriesCompanyStockData.as_view(), name='company_stock'),
]
