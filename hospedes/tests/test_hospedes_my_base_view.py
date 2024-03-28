from hospedes import views
from django.http import Http404

from usuarios.tests.test_usuarios_base import BaseTestMixin


class HospedesMyBaseViewTest(BaseTestMixin):
    def test_hospedes_my_base_view_return_404_if_not_hospede(self):
        view = views.MyBaseView()

        hospede = self.make_full_hospede_no_login()
        fake_hospede_id = hospede.id + 333333

        with self.assertRaises(Http404):
            view.get_hospede(fake_hospede_id)

    def test_hospedes_my_base_view_return_hospede(self):
        view = views.MyBaseView()

        hospede = self.make_full_hospede_no_login()
        id_test = view.get_hospede(hospede.id)

        self.assertEqual(
            id_test.id, hospede.id
        )
