import factory
from factory import post_generation

from stock_exchange.apps.company.models import User


class UserFactory(factory.DjangoModelFactory):
    email = factory.Sequence(lambda n: "person{0}@example.com".format(n))

    @post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password("password")

    class Meta:
        model = User
