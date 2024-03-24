import factory

from sekura import factories

from . import models


class RiskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Risk

    title = factory.Faker("sentence")
    description = factory.Faker("text")
    likelyhood = factory.Faker("pyint", min_value=0, max_value=10)
    impact = factory.Faker("pyint", min_value=0, max_value=10)
    owner = factory.SubFactory(factories.UserFactory)
