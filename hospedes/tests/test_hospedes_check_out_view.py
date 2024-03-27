from hospedes import views

from django.urls import reverse, resolve

from usuarios.tests.test_usuarios_base import (
    BaseTestMixin,
)


class HospedesCheckOutViewTest(BaseTestMixin):

    def test_hospedes_check_out_view_function_is_correct(self):
        hospede = self.make_full_hospede_no_login()

        view = resolve(
            reverse(
                'hospedes:check_out', kwargs={'id': hospede.id}
            )
        )
        self.assertIs(view.func, views.check_out)

    def test_hospedes_check_out_view_returns_statuscode_200_if_logged(self):
        hospede = self.make_full_hospede_with_login()

        response = self.client.get(
            reverse(
                'hospedes:check_out', kwargs={'id': hospede.id}
            )
        )

        self.assertEqual(response.status_code, 200)\


    def test_hospedes_check_out_view_returns_statuscode_302_if_not_logged(self):  # noqa: E501
        hospede = self.make_full_hospede_no_login()

        response = self.client.get(
            reverse(
                'hospedes:check_out', kwargs={'id': hospede.id}
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_hospedes_check_out_view_redirect_after_statuscode_302_if_not_logged(self):  # noqa: E501
        hospede = self.make_full_hospede_no_login()

        response = self.client.get(
            reverse(
                'hospedes:check_out', kwargs={'id': hospede.id}
            )
        )

        self.assertEqual(response.status_code, 302)
        # Aqui vem o verdadeiro teste
        self.assertRedirects(
            response, response.url
        )

    def test_hospedes_check_out_view_loads_correct_template(self):
        hospede = self.make_full_hospede_with_login()

        response = self.client.get(
            reverse(
                'hospedes:check_out', kwargs={'id': hospede.id}
            )
        )

        self.assertTemplateUsed(
            response, 'checkout.html'
        )

    def test_hospedes_check_out_view_raises_404_if_dont_find_hospede(self):
        hospede = self.make_full_hospede_with_login()

        fake_id = hospede.id + 22222

        response = self.client.get(
            reverse(
                'hospedes:check_out', kwargs={'id': fake_id}
            )
        )

        self.assertEqual(
            response.status_code, 404
        )

    def test_hospedes_check_out_view_loads_context_hospede_if_request_method_get(self):  # noqa: E501
        hospede = self.make_full_hospede_with_login()

        response = self.client.get(
            reverse(
                'hospedes:check_out', kwargs={'id': hospede.id}
            )
        )

        self.assertIn(
            'hospede', response.context
        )

        self.assertContains(
            response, 'Informações da Estadia'
        )

    def test_hospedes_check_out_view_make_check_out_and_redirect_to_index(self):  # noqa: E501
        hospede = self.make_full_hospede_with_login()

        url = reverse(
            'hospedes:check_out',
            kwargs={'id': hospede.id}
        )

        response = self.client.post(
            url,
            data={'action': 'check_out'},
            follow=True
        )

        self.assertRedirects(
            response, '/'
        )

        self.assertContains(
            response, 'Check-Out realizado com sucesso!'
        )

    def test_hospedes_check_out_view_got_wrong_action(self):
        hospede = self.make_full_hospede_with_login()

        url = reverse(
            'hospedes:check_out',
            kwargs={'id': hospede.id}
        )

        response = self.client.post(
            url,
            data={'action': 'check'},
            follow=True
        )

        self.assertIn(
            'hospede', response.context
        )

    def test_hospedes_check_out_view_make_check_out_and_hospede_status_now_is_checkout_realizado(self):  # noqa: E501
        hospede = self.make_full_hospede_with_login()
        hospede.status = "EM_ESTADIA"
        hospede.save()

        url = reverse(
            'hospedes:check_out',
            kwargs={'id': hospede.id}
        )

        self.client.post(
            url,
            data={'action': 'check_out'},
            follow=True
        )

        # recarregando com os dados apos a execuçao do post!
        hospede.refresh_from_db()

        self.assertEqual(
            hospede.status, 'CHECKOUT_REALIZADO'
        )
