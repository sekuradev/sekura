from django.test import (
    TestCase,
    Client,
)
from django.urls import reverse


class SecurityTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_forbidden(self):
        r = self.client.get(reverse("contact:index"))
        self.assertRedirects(r, "/account/login/?next=/contact/")

    def test_detail_forbidden(self):
        r = self.client.get(reverse("contact:detail", kwargs={"pk": 1}))
        self.assertRedirects(r, "/account/login/?next=/contact/1/")

    def test_edit_forbidden(self):
        r = self.client.get(reverse("contact:edit", kwargs={"pk": 1}))
        self.assertRedirects(r, "/account/login/?next=/contact/1/edit/")

    def test_create_forbidden(self):
        r = self.client.get(reverse("contact:create"))
        self.assertRedirects(r, "/account/login/?next=/contact/create/")
