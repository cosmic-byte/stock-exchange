import os
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "stock_exchange.settings"))
import django

django.setup()
logger = logging.getLogger(__name__)
from django.contrib.auth import get_user_model

from django.utils import timezone

from stock_exchange.apps.company.models import Company
from stock_exchange.apps.stock.models import Stock

User = get_user_model()
import factory
from factory import post_generation, Faker, fuzzy


class UserFactory(factory.DjangoModelFactory):
    email = factory.Sequence(lambda n: "person{0}@example.com".format(n + 1))

    @post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password("password")

    class Meta:
        model = User


class CompanyFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    ref_first_name = Faker('first_name')
    ref_last_name = Faker('last_name')
    company_name = Faker('name')
    company_symbol = fuzzy.FuzzyText(length=3)

    class Meta:
        model = Company


class StockFactory(factory.DjangoModelFactory):
    open_amount_in_ngn = factory.Sequence(lambda n: n + 10)
    high_amount_in_usd = factory.Sequence(lambda n: n + 20)
    low_amount_in_usd = factory.Sequence(lambda n: n)
    close_amount_in_usd = factory.Sequence(lambda n: n + 15)
    volume_amount_in_usd = factory.Sequence(lambda n: n * 1000)
    company = factory.SubFactory(CompanyFactory)
    data_time = fuzzy.FuzzyDateTime(timezone.now(), force_year=2020)

    class Meta:
        model = Stock


def seed_data():
    companies = CompanyFactory.create_batch(2)
    for company in companies:
        logger.warning(f'Filling Data - {company.company_name}')
        StockFactory.create_batch(20, company=company)
    return companies


if __name__ == '__main__':
    seed_data()
