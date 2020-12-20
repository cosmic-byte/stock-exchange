import factory

from stock_exchange.apps.app_admin.models import AppAdmin
from stock_exchange.tests.company.factories import UserFactory


class AppAdminFactory(factory.DjangoModelFactory):
    first_name = 'App'
    last_name = 'Admin'
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = AppAdmin
