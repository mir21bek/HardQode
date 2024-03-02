import factory
from factory.django import DjangoModelFactory
from courses.models import Product, Group
from Factory.users.factory_user import CustomUserFactory


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    product_name = "Test Product"
    price = 2400.00
    start_time = factory.Faker("date_time", tzinfo=None)
    author = factory.SubFactory(CustomUserFactory)


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    group_name = "Test Group"
    product = factory.SubFactory(ProductFactory)
    min_users = 5
    max_users = 15
