import factory
from faker import Faker

from . import models

fake = Faker()


class RiskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Risk

    title = factory.LazyFunction(fake.sentence)
    description = factory.LazyFunction(fake.text)
    likelyhood = fake.pyint(0, 10)
    impact = fake.pyint(0, 10)
