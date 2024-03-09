from django.test import Client, TestCase
from django.urls import reverse


class SecurityTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_forbidden(self):
        r = self.client.get(reverse("archive:index"))
        self.assertRedirects(r, "/account/login/?next=/archive/")

    def test_detail_forbidden(self):
        r = self.client.get(reverse("archive:detail", kwargs={"pk": 1}))
        self.assertRedirects(r, "/account/login/?next=/archive/1/")

    def test_edit_forbidden(self):
        r = self.client.get(reverse("archive:edit", kwargs={"pk": 1}))
        self.assertRedirects(r, "/account/login/?next=/archive/1/edit/")

    def test_create_forbidden(self):
        r = self.client.get(reverse("archive:create"))
        self.assertRedirects(r, "/account/login/?next=/archive/create/")
