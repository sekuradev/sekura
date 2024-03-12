import tempfile
from io import StringIO

from bs4 import BeautifulSoup
from django.conf import settings
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
        self.archive = factories.ArchiveFactory()
        settings.MEDIA_ROOT = tempfile.mkdtemp()

    def test_get_returns_form(self):
        # GIVEN
        # WHEN
        r = self.client.get(reverse("archive:edit", kwargs={"pk": self.archive.pk}))

        # THEN
        soup = BeautifulSoup(r.content, features="html.parser")

        assert soup.form.get("action") == f"/archive/{self.archive.pk}/edit/"
        assert soup.form.get("method") == "post"
        assert soup.form.get("enctype") == "multipart/form-data"

        csrf = soup.form.find("input", {"name": "csrfmiddlewaretoken"})
        assert csrf.get("type") == "hidden"

    def test_post_same_content(self):
        # GIVEN
        data = model_to_dict(self.archive)
        data["content"] = StringIO("This is a content")

        # WHEN
        r = self.client.post(reverse("archive:edit", kwargs={"pk": self.archive.pk}), data)
        # THEN
        assert isinstance(r, HttpResponseRedirect)
        assert r.url == reverse("archive:detail", kwargs={"pk": self.archive.pk})

    def test_post_invalid_form(self):
        # GIVEN
        data = model_to_dict(self.archive)
        data["content"] = StringIO("This is a content")
        data["name"] = 10000 * "a"

        # WHEN
        r = self.client.post(reverse("archive:edit", kwargs={"pk": self.archive.pk}), data)
        # THEN
        assert b"invalid-feedback" in r.content
