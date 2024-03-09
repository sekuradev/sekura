from django import forms

from . import models


class Risk(forms.ModelForm):
    class Meta:
        model = models.Risk
        exclude = ["creation", "update"]
