from django.urls import reverse, resolve

from usuarios import views

from .test_usuarios_base import BaseTestMixin, timezone


class UsuariosIndexTest(BaseTestMixin):

    def test_usuarios_index_views_function_is_correct(self):
        view = resolve(
            reverse(
                'index'
            )
        )
        self.assertIs(view.func.view_class, views.IndexView)

    def test_usuarios_index_view_returns_statuscode_200_if_logged(self):

        user = self.get_user()
        self.client.login(
            username=user.username,
            password='12345'
        )

        response = self.client.get(
            reverse(
                'index'
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_usuarios_index_view_returns_statuscode_302_if_not_logged(self):
        response = self.client.get(
            reverse(
                'index'
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_usuarios_index_view_redirect_after_statuscode_302_if_not_logged(self):  # noqa: E501
        response = self.client.get(
            reverse(
                'index'
            )
        )

        self.assertEqual(response.status_code, 302)
        # o verdadeiro test
        self.assertRedirects(
            response, response.url
        )

    def test_usuarios_index_view_loads_correct_template(self):
        user = self.get_user()
        self.client.login(
            username=user.username,
            password='12345'
        )

        response = self.client.get(
            reverse(
                'index'
            )
        )

        self.assertTemplateUsed(
            response, 'index.html'
        )

    def test_usuarios_index_view_context_variables(self):
        user = self.get_user()
        self.client.login(
            username=user.username,
            password='12345'
        )

        response = self.client.get(
            reverse(
                'index'
            )
        )

        # fazendo algumas verificações para ver se nossas variaveis estão
        # presentes no contexto
        self.assertContains(
            response,
            'Início da dashboard'
        )
        self.assertContains(
            response,
            'Informações do hotel'
        )
        self.assertIn(
            'reservas_proximas',
            response.context
        )

    def test_usuarios_index_view_correct_logic_of_dashboard_stuff(self):
        user = self.get_user(username='userzz')
        self.client.login(
            username=user.username,
            password='12345'
        )
        self.make_porteiro(usuario=user)

        hoje = timezone.now().date()

        hospede = self.make_hospede()
        self.make_reserva(
            nome_hospede=hospede.nome_completo,
            registrado_por=hospede.registrado_por,
            horario_checkin=hoje,
            horario_checkout=hoje,
            status_reserva='CONFIRMADO'
        )
        self.make_quarto()

        response = self.client.get(
            reverse(
                'index'
            )
        )

        # verificando algumas logicas de contexto da view
        self.assertEqual(
            response.context['checkin_hoje'].first().horario_checkin.date(),
            hoje
        )
        self.assertEqual(
            response.context['checkin_hoje'].first().horario_checkout.date(),
            hoje
        )

        self.assertEqual(
            response.context['reservas'].first().nome_hospede.nome_completo,
            "Nome completo"
        )
