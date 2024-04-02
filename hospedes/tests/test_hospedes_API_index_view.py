from django.urls import reverse, resolve

from usuarios.tests.test_usuarios_base import timezone

from hospedes.views import api
from .test_hospedes_API_base import APIBaseTestMixin


class TestIndexAPIView(APIBaseTestMixin):

    def test_index_api_view_function_is_correct(self):
        view = resolve(
            reverse('hospedes:index_api')
        )

        self.assertIs(view.func.view_class, api.IndexAPIView)

    def test_index_api_view_return_code_401_if_not_logged(self):
        api_url = reverse(
            'hospedes:index_api'
        )

        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 401)

    def test_index_api_view_return_code_200_if_authenticated(self):
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url = reverse(
            'hospedes:index_api'
        )

        response = self.client.get(
            api_url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # checando se foi recebido um code 200
        # (mostrando que usuario esta logado e pode ver a index)
        self.assertEqual(response.status_code, 200)

    def test_index_api_will_receive_code_405_if_method_is_not_get(self):
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url = reverse(
            'hospedes:index_api'
        )

        response = self.client.post(
            api_url,
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # verificando se recebe um code 405 (método nao permitido)
        # pois essa view só recebe "GET"
        self.assertEqual(response.status_code, 405)

    def test_index_api_returns_the_right_data(self):
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url = reverse(
            'hospedes:index_api'
        )

        response = self.client.get(
            api_url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # Checando se tudo que foi passado como data esta contido no retorno
        # da função
        self.assertIn('inicio_dashboard', response.data)
        self.assertIn('nome_pagina', response.data)

    def test_index_api_correct_logic_of_dashboard(self):
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')
        # pegando porteiro

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

        api_url = reverse(
            'hospedes:index_api'
        )

        response = self.client.get(
            api_url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # Acessando o primeiro item da lista
        checkin_hoje = response.data['checkin_hoje'][0]
        # verificando algumas logicas de contexto da view
        self.assertEqual(
            # Considerar apenas os 10 primeiros caracteres, que representam
            # a datacheckin_hoje['horario_checkin'],
            checkin_hoje['horario_checkin'][:10],
            str(hoje)
        )

        self.assertEqual(response.data['total_reservas'], 1)
