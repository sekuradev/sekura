from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker
from guardian.shortcuts import assign_perm

from .. import models

fake = Faker()


class CreateTest(TestCase):
    def setUp(self):
        login = fake.email()
        pwd = fake.password()
        self.user = User.objects.create_user(username=login, password=pwd)
        self.client = Client()
        self.client.login(username=login, password=pwd)

    def test_get_returns_form(self):
        # GIVEN
        assign_perm(models.RiskPermissions.ADD, self.user)

        # WHEN
        r = self.client.get(reverse("risk:create"))

        # THEN
        soup = BeautifulSoup(r.content, features="html.parser")

        assert soup.form.get("action") == "/risk/create/"
        assert soup.form.get("method") == "post"

        csrf = soup.form.find("input", {"name": "csrfmiddlewaretoken"})
        assert csrf.get("type") == "hidden"

    def test_post_empty_returns_invalid_form(self):
        # GIVEN
        assign_perm(models.RiskPermissions.ADD, self.user)

        # WHEN
        r = self.client.post(reverse("risk:create"))

        # THEN
        assert b"This field is required." in r.content

    def test_post_valid(self):
        # GIVEN
        assign_perm(models.RiskPermissions.ADD, self.user)
        # WHEN
        self.client.post(
            reverse("risk:create"),
            {
                "title": fake.sentence(),
                "description": fake.text(),
                "likelyhood": fake.pyint(0, 10),
                "impact": fake.pyint(0, 10),
            },
        )
        # THEN
        assert models.Risk.objects.count() == 1
