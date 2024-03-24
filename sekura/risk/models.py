from django.contrib.auth import get_user_model
from django.db import models
from guardian.shortcuts import assign_perm, get_objects_for_user, remove_perm


class RiskPermissions:
    VIEW = "view_risk"
    CHANGE = "change_risk"
    DELETE = "delete_risk"
    ADD = "add_risk"

    @classmethod
    def tuple(cls):
        return (cls.VIEW, cls.CHANGE)


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
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_owner = self.owner

    @property
    def score(self):
        return int(self.likelyhood * self.impact / 10)

    def __str__(self):
        return self.title

    def allow_view(self, user):
        assign_perm(RiskPermissions.VIEW, user, self)

    def allow_change(self, user):
        assign_perm(RiskPermissions.CHANGE, user, self)

    @classmethod
    def get_for_user(cls, user):
        return get_objects_for_user(user, RiskPermissions.VIEW, cls)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.owner != self._original_owner:
            for perm in (RiskPermissions.VIEW, RiskPermissions.CHANGE, RiskPermissions.DELETE):
                remove_perm(perm, self._original_owner, self)
                assign_perm(perm, self.owner, self)
