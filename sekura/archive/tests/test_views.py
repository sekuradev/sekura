from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ListTest(TestCase):
    def setUp(self):
        login = "foo"
        pwd = "foo"
        user = User.objects.create_user(username=login, password=pwd)
        self.client = Client()
        self.client.login(username=login, password=pwd)

    def test_no_archives(self):
        r = self.client.get(reverse("archive:index"))
        assert r.status_code == 200
        assert b"No archives are available" in r.content
