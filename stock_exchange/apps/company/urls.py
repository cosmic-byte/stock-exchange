from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import (
    ObtainJSONWebToken,
    RefreshJSONWebToken
)
from stock_exchange.apps.company import views
from stock_exchange.auth import JWTSerializer, JWTRefreshTokenSerializer

app_name = 'company'

urlpatterns = [
    url(r'^create/$', views.CompanyCreateView.as_view(), name='create_company'),
    url(r'^(?P<pk>[0-9a-f-]+)/details/$', views.RetrieveCompanyDetailsById.as_view(), name='retrieve_company'),
    url(r'^(?P<pk>[0-9a-f-]+)/update/$', views.UpdateCompanyView.as_view(), name='update_company'),
    url(r'^$', views.ListCompanyView.as_view(), name='list_companies'),
    path('<uuid:pk>/delete', views.DeleteCompanyView.as_view(), name='delete_company'),
    path('login', ObtainJSONWebToken.as_view(serializer_class=JWTSerializer), name='login'),
    path('api-token-refresh', RefreshJSONWebToken.as_view(serializer_class=JWTRefreshTokenSerializer), name='refresh')
]
