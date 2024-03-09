from django.contrib import admin

from . import models

admin.site.register(models.Archive)
admin.site.register(models.Category)
