from stock_exchange.apps.app_admin.views import AdminViewSet
from stock_exchange.custom_router_retrieve_has_no_param import CustomRouterRetrieveHasNoParam

app_name = 'app_admin'

router = CustomRouterRetrieveHasNoParam()
router.register(r'', AdminViewSet, basename='app_admin')

urlpatterns = router.urls
