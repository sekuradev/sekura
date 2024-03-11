import factory

from .. import models


class ArchiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Archive

    name = factory.Sequence(lambda n: "archive%d" % n)
