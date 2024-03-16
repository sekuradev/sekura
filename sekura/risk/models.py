from django.db import models


class Risk(models.Model):
    TREATMENTS = {
        "M": "Mitigate",
        "T": "Transfer",
        "A": "Avoid",
        "C": "Accept",
    }
    title = models.CharField(max_length=100)
    description = models.TextField()
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    likelyhood = models.PositiveIntegerField()
    impact = models.PositiveIntegerField()
    treatment = models.CharField(max_length=3, choices=TREATMENTS, null=True, blank=True)
    confidentiality = models.BooleanField(default=False)
    integrity = models.BooleanField(default=False)
    availability = models.BooleanField(default=False)
    custom_id = models.CharField(max_length=20, blank=True, null=True)

    def risk(self):
        return int(self.likelyhood * self.impact / 10)

    def __str__(self):
        return self.title
