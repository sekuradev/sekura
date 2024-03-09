from django import forms

from . import models


class Vendor(forms.ModelForm):
    class Meta:
        model = models.Vendor
        exclude = ["creation", "update"]
