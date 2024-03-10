import tempfile
from io import StringIO

from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .. import models


class CreateTest(TestCase):
    def setUp(self):
        login = "foo"
        pwd = "foo"
        User.objects.create_user(username=login, password=pwd)
        self.client = Client()
        self.client.login(username=login, password=pwd)
        settings.MEDIA_ROOT = tempfile.mkdtemp()

    def test_get_returns_form(self):
        # GIVEN

        # WHEN
        r = self.client.get(reverse("archive:create"))

        # THEN
        soup = BeautifulSoup(r.content, features="html.parser")

        assert soup.form.get("action") == "/archive/create/"
        assert soup.form.get("method") == "post"
        assert soup.form.get("enctype") == "multipart/form-data"

        csrf = soup.form.find("input", {"name": "csrfmiddlewaretoken"})
        assert csrf.get("type") == "hidden"

    def test_post_empty_returns_invalid_form(self):
        # GIVEN

        # WHEN
        r = self.client.post(reverse("archive:create"))

        # THEN
        assert b"This field is required." in r.content

    def test_post_valid(self):
        # GIVEN
        fd = StringIO("This is a test")

        # WHEN
        self.client.post(reverse("archive:create"), {"name": "test", "content": fd})

        # THEN
        assert models.Archive.objects.count() == 1
