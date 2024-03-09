from django.test import (
    TestCase,
    Client,
)
from django.urls import reverse


class SecurityTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_forbidden(self):
        r = self.client.get(reverse("risk:index"))
        self.assertRedirects(r, "/account/login/?next=/risk/")

    def test_detail_forbidden(self):
        r = self.client.get(reverse("risk:detail", kwargs={"pk": 1}))
        self.assertRedirects(r, "/account/login/?next=/risk/1/")

    def test_edit_forbidden(self):
        r = self.client.get(reverse("risk:edit", kwargs={"pk": 1}))
        self.assertRedirects(r, "/account/login/?next=/risk/1/edit/")

    def test_create_forbidden(self):
        r = self.client.get(reverse("risk:create"))
        self.assertRedirects(r, "/account/login/?next=/risk/create/")
