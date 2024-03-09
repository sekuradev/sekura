from django.test import Client, TestCase
from django.urls import reverse


class SecurityTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_forbidden(self):
        r = self.client.get(reverse("vendor:index"))
        self.assertRedirects(r, "/account/login/?next=/vendor/")

    def test_detail_forbidden(self):
        r = self.client.get(reverse("vendor:detail", kwargs={"pk": 1}))
        self.assertRedirects(r, "/account/login/?next=/vendor/1/")

    def test_edit_forbidden(self):
        r = self.client.get(reverse("vendor:edit", kwargs={"pk": 1}))
        self.assertRedirects(r, "/account/login/?next=/vendor/1/edit/")

    def test_create_forbidden(self):
        r = self.client.get(reverse("vendor:create"))
        self.assertRedirects(r, "/account/login/?next=/vendor/create/")
