from django import forms

from . import models


class Archive(forms.ModelForm):
    class Meta:
        model = models.Archive
        exclude = ["creation", "update"]
