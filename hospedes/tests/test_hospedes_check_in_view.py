from hospedes import views

from datetime import timedelta

from django.urls import reverse, resolve

from usuarios.tests.test_usuarios_base import (
    BaseTestMixin,
)


class HospedesCheckInViewTest(BaseTestMixin):
    def test_hospedes_check_in_view_function_is_correct(self):
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()

        view = resolve(
            reverse(
                'hospedes:check_in', kwargs={'id': hospede.id}
            )
        )
        self.assertIs(view.func, views.check_in)

    def test_hospedes_check_in_view_returns_statuscode_200_if_logged(self):

        user = self.get_user()
        self.client.login(
            username=user.username,
            password='12345'
        )
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()

        response = self.client.get(
            reverse(
                'hospedes:check_in', kwargs={'id': hospede.id}
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_hospedes_check_in_view_returns_statuscode_302_if_not_logged(self):
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()

        response = self.client.get(
            reverse(
                'hospedes:check_in', kwargs={'id': hospede.id}
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_hospedes_check_in_view_redirect_after_statuscode_302_if_not_logged(self):  # noqa: E501
        user = self.get_user()
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()

        response = self.client.get(
            reverse(
                'hospedes:check_in', kwargs={'id': hospede.id}
            )
        )

        self.assertEqual(response.status_code, 302)
        # Aqui vem o verdadeiro teste
        self.assertRedirects(
            response, response.url
        )

    def test_hospedes_check_in_view_loads_correct_template(self):
        user = self.get_user()
        self.client.login(
            username=user.username,
            password='12345'
        )
        self.make_porteiro(usuario=user)
        hospede = self.make_hospede()

        response = self.client.get(
            reverse(
                'hospedes:check_in', kwargs={'id': hospede.id}
            )
        )

        self.assertTemplateUsed(
            response, 'checkin.html'
        )
