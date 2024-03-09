from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_staff = models.BooleanField(default=True)

    def as_text(self):
        if self.email:
            return f"{self.name} <{self.email}>"
        return self.name

    def __str__(self):
        staff = "(staff)" if self.is_staff else "(external)"
        return self.as_text() + staff
