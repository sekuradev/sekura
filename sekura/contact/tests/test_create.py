from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker

from .. import models

fake = Faker()


class CreateTest(TestCase):
    def setUp(self):
        login = "foo"
        pwd = "foo"
        User.objects.create_user(username=login, password=pwd)
        self.client = Client()
        self.client.login(username=login, password=pwd)

    def test_get_returns_form(self):
        # GIVEN
        # WHEN
        r = self.client.get(reverse("contact:create"))

        # THEN
        soup = BeautifulSoup(r.content, features="html.parser")

        assert soup.form.get("action") == "/contact/create/"
        assert soup.form.get("method") == "post"

        csrf = soup.form.find("input", {"name": "csrfmiddlewaretoken"})
        assert csrf.get("type") == "hidden"

    def test_post_empty_returns_invalid_form(self):
        # GIVEN

        # WHEN
        r = self.client.post(reverse("contact:create"))

        # THEN
        assert b"This field is required." in r.content

    def test_post_valid(self):
        # GIVEN
        # WHEN
        self.client.post(reverse("contact:create"), {"name": fake.name(), "email": fake.email()})

        # THEN
        assert models.Contact.objects.count() == 1
