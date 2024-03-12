import factory

from .. import models


class VendorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Vendor

    name = factory.Sequence(lambda n: "vendor%s" % n)
