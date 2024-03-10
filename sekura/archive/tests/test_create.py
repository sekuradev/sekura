from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from io import StringIO
from django.conf import settings
import tempfile

from .. import models

class CreateTest(TestCase):
    def setUp(self):
        login = "foo"
        pwd = "foo"
        user = User.objects.create_user(username=login, password=pwd)
        self.client = Client()
        self.client.login(username=login, password=pwd)
        settings.MEDIA_ROOT = tempfile.mkdtemp()


    def test_get_returns_form(self):
        r = self.client.get(reverse("archive:create"))

        soup = BeautifulSoup(r.content, features="html.parser")

        assert soup.form.get("action") == "/archive/create/"
        assert soup.form.get("method")== "post"
        assert soup.form.get("enctype") == "multipart/form-data"

        csrf = soup.form.find("input", {"name": "csrfmiddlewaretoken"})
        assert csrf.get("type") == "hidden"

    def test_post_empty_returns_invalid_form(self):
        r = self.client.post(reverse("archive:create"))
        assert b"This field is required." in r.content

    def test_post_valid(self):
        fd = StringIO("This is a test")
        r = self.client.post(reverse("archive:create"), {"name": "test", "content": fd})
        assert models.Archive.objects.count() == 1
