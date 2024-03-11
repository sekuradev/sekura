from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.test import Client, TestCase
from django.urls import reverse

from . import factories


class EditTest(TestCase):
    def setUp(self):
        login = "foo"
        pwd = "foo"
        User.objects.create_user(username=login, password=pwd)
        self.client = Client()
        self.client.login(username=login, password=pwd)
        self.risk = factories.RiskFactory()

    def test_get_returns_form(self):
        # GIVEN
        # WHEN
        r = self.client.get(reverse("risk:edit", kwargs={"pk": self.risk.pk}))

        # THEN
        soup = BeautifulSoup(r.content, features="html.parser")

        assert soup.form.get("action") == f"/risk/{self.risk.pk}/edit/"
        assert soup.form.get("method") == "post"

        csrf = soup.form.find("input", {"name": "csrfmiddlewaretoken"})
        assert csrf.get("type") == "hidden"

    def test_post_same_values(self):
        # GIVEN
        data = model_to_dict(self.risk)
        del data["treatment"]
        del data["custom_id"]

        # WHEN
        r = self.client.post(reverse("risk:edit", kwargs={"pk": self.risk.pk}), data)
        print(r.content)
        # THEN
        assert isinstance(r, HttpResponseRedirect)
        assert r.url == reverse("risk:detail", kwargs={"pk": self.risk.pk})

    def test_post_invalid_form(self):
        # GIVEN
        data = model_to_dict(self.risk)
        data["title"] = 10000 * "a"
        del data["treatment"]
        del data["custom_id"]

        # WHEN
        r = self.client.post(reverse("risk:edit", kwargs={"pk": self.risk.pk}), data)
        # THEN
        assert b"invalid-feedback" in r.content
