import factory
from factory.django import DjangoModelFactory
from faker import Faker
from users.models import CustomUser

fake = Faker()


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    user_name = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda _: fake.email())
