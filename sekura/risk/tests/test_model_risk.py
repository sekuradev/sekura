from django.test import TestCase

from sekura import factories as global_factories

from .. import factories, models


class RiskModelTest(TestCase):
    def test_title(self):
        # GIVEN
        risk = factories.RiskFactory.create()

        # WHEN
        title = str(risk)

        # THEN
        assert title == risk.title

    def test_score(self):
        # GIVEN
        risk = factories.RiskFactory.create(likelyhood=4, impact=6)
        print(risk.likelyhood)
        print(risk.impact)

        # WHEN/THEN
        assert risk.score == 2

    def test_permission_owner(self):
        # GIVEN
        user = global_factories.UserFactory.create()
        risk = factories.RiskFactory.create()
        risk.set_owner(user)

        # WHEN
        risk_list = list(models.Risk.get_for_user(user))

        # THEN
        assert len(risk_list) == 1
        assert risk_list[0].title == risk.title
        assert risk_list[0].description == risk.description

    def test_permission_view_all(self):
        # GIVEN
        user1 = global_factories.UserFactory.create()
        user2 = global_factories.UserFactory.create()
        risk = factories.RiskFactory.create()
        risk.set_owner(user1)
        risk.allow_view(user2)

        # WHEN
        risk_list = list(models.Risk.get_for_user(user2))

        # THEN
        assert len(risk_list) == 1
        assert risk_list[0].title == risk.title
        assert risk_list[0].description == risk.description
