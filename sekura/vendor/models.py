from django.db import models


class Datatype(models.Model):
    name = models.CharField(max_length=30)
    required_archive_categories = models.ManyToManyField("archive.Category", blank=True)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=100, help_text="Vendor's name")
    url = models.URLField(blank=True, null=True)
    account_manager = models.ForeignKey(
        "contact.Contact",
        limit_choices_to={"is_staff": False},
        related_name="vendors_as_account_manager",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    contact = models.ForeignKey(
        "contact.Contact",
        limit_choices_to={"is_staff": True},
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    datatypes = models.ManyToManyField(Datatype, blank=True)

    def __str__(self):
        return self.name

    def required_datatype_files(self):
        result = set()
        for dt in self.datatypes.all():
            for category in dt.required_archive_categories.all():
                result.add(category)
        return result


class Review(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return self.creation
