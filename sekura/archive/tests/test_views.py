from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class ListTest(TestCase):
    def setUp(self):
        login = "foo"
        pwd = "foo"
        User.objects.create_user(username=login, password=pwd)
        self.client = Client()
        self.client.login(username=login, password=pwd)

    def test_no_archives(self):
        # GIVEN

        # WHEN
        r = self.client.get(reverse("archive:index"))

        # THEN
        assert r.status_code == 200
        assert b"No archives are available" in r.content
