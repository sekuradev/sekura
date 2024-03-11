import factory
from faker import Faker

from .. import models

fake = Faker()


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Contact

    name = factory.Sequence(lambda n: "archive%d" % n)
    email = fake.email()
    notes = fake.sentence()
