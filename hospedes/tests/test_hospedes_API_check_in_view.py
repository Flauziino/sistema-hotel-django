from django.contrib import messages
from django.urls import reverse, resolve

from hospedes.views import api
from hospedes.models import Hospede
from .test_hospedes_API_base import APIBaseTestMixin


class TestCheckInAPIView(APIBaseTestMixin):
    def test_check_in_api_view_function_is_correct(self):
        view = resolve(
            reverse('hospedes:check_in_api', kwargs={'id': 1})
        )
        self.assertIs(view.func.view_class, api.CheckInAPIView)

    def test_check_in_api_view_returns_code_401_if_not_authenticated(self):  # noqa: E501
        api_url = reverse('hospedes:check_in_api', kwargs={'id': 1})
        response = self.client.post(
            api_url,
            data={}
        )
        self.assertEqual(response.status_code, 401)

    def test_check_in_api_view_will_receive_code_405_if_method_is_put(self):
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url = reverse('hospedes:check_in_api', kwargs={'id': 1})
        # passando metodo put buscando uma falha
        response = self.client.put(
            api_url,
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # verificando se recebe um code 405 (método nao permitido)
        # pois essa view só recebe "POST e GET"
        self.assertEqual(response.status_code, 405)

    def test_check_in_api_view_will_receive_code_405_if_method_is_patch(self):
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url = reverse('hospedes:check_in_api', kwargs={'id': 1})
        # passando metodo patch buscando uma falha
        response = self.client.patch(
            api_url,
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # verificando se recebe um code 405 (método nao permitido)
        # pois essa view só recebe "POST e GET"
        self.assertEqual(response.status_code, 405)

    def test_check_in_api_view_will_receive_code_405_if_method_is_delete(self):
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url = reverse('hospedes:check_in_api', kwargs={'id': 1})
        # passando metodo delete buscando uma falha
        response = self.client.delete(
            api_url,
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # verificando se recebe um code 405 (método nao permitido)
        # pois essa view só recebe "POST e GET"
        self.assertEqual(response.status_code, 405)

    def test_check_in_api_view_will_return_404_if_not_hospede_method_get(self):
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        hospede = {
            "id": 1,
            "nome_completo": "TEST",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "status": "AGUARDANDO_CHECKIN",
            "horario_checkin": "2024-04-25T00:00:00-03:00",
            "registrado_por": 1,
            "action": "check_in"
        }

        fake_id = hospede.get('id') + 9999999

        api_url = reverse('hospedes:check_in_api', kwargs={'id': fake_id})
        # passando metodo delete buscando uma falha
        response = self.client.get(
            api_url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # verificando se recebe um code 404
        self.assertEqual(response.status_code, 404)

    def test_check_in_api_view_will_return_404_if_not_hospede_method_post(self):  # noqa: E501
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        hospede = {
            "id": 1,
            "nome_completo": "TEST",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "status": "AGUARDANDO_CHECKIN",
            "horario_checkin": "2024-04-25T00:00:00-03:00",
            "registrado_por": 1,
            "action": "check_in"
        }

        fake_id = hospede.get('id') + 9999999

        api_url = reverse('hospedes:check_in_api', kwargs={'id': fake_id})
        # passando metodo delete buscando uma falha
        response = self.client.post(
            api_url,
            data=hospede,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # verificando se recebe um code 404
        self.assertEqual(response.status_code, 404)

    def test_check_in_api_view_will_return_400_if_action_not_check_in_or_cancelar_reserva(self):  # noqa: E501
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url_hospede = reverse('hospedes:criar_hospede_api')
        self.make_quarto()
        # criando os dados para o hospede em JSON
        data_hospede = {
            "nome_completo": "Hospede 1 Test",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "horario_checkin": "2024-04-25",
            "horario_checkout": "2024-05-28",
            "registrado_por": "1"
        }

        response = self.client.post(
            api_url_hospede,
            data=data_hospede,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # checando se foi recebido um code 201
        # (mostrando que usuario esta logado e criou um hospede com sucesso)
        self.assertEqual(response.status_code, 201)
        # verificando se a msg de sucesso esta contida
        self.assertIn(
            'Reserva do hóspede registrada com sucesso!',
            [msg.message for msg in messages.get_messages(response.wsgi_request)])  # noqa: E501

        # com hospede criado agora é simular a criaçao de uma reserva
        api_url_reserva = reverse('hospedes:realizar_reserva_api')
        data_reserva = {
            "forma_pagamento": "TED",
            "status_reserva": "CONFIRMADO",
            "registrado_por": "1",
            "horario_checkin": "2024-04-25",
            "horario_checkout": "2024-05-28",
            "quartos": ["1"]
        }
        response_reserva = self.client.post(
            api_url_reserva,
            data=data_reserva,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao
        # checando se foi recebido um code 201
        # (mostrando que usuario esta logado e criou uma reserva para o hospede)  # noqa: E501
        self.assertEqual(response_reserva.status_code, 201)
        # checando se o status da reserva esta como "CONFIRMADO"
        self.assertEqual(
            response_reserva.data["status_reserva"],
            "CONFIRMADO"
        )

        hospede = Hospede.objects.all().first()
        api_url = reverse(
            'hospedes:check_in_api',
            kwargs={'id': hospede.id}
        )
        # agora simular realizar checkin recebendo um action diferente de
        # check_in ou de cancelar_reserva
        data_checkin = {
            "id": 1,
            "nome_completo": "TEST",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "status": "AGUARDANDO_CHECKIN",
            "horario_checkin": "2024-04-25T00:00:00-03:00",
            "registrado_por": 1,
            "action": "check"
        }

        response = self.client.post(
            api_url,
            data=data_checkin,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao
        # checando se a msg de error esta na resposta
        self.assertEqual(
            response.data['error'],
            'Algo deu errado!'
        )
        self.assertEqual(response.status_code, 400)

    def test_check_in_api_view_will_return_hospede_data_if_get_method(self):
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url_hospede = reverse('hospedes:criar_hospede_api')
        self.make_quarto()
        # criando os dados para o hospede em JSON
        data_hospede = {
            "nome_completo": "Hospede 1 Test",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "horario_checkin": "2024-04-25",
            "horario_checkout": "2024-05-28",
            "registrado_por": "1"
        }

        response = self.client.post(
            api_url_hospede,
            data=data_hospede,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # checando se foi recebido um code 201
        # (mostrando que usuario esta logado e criou um hospede com sucesso)
        self.assertEqual(response.status_code, 201)
        hospede = Hospede.objects.all().first()
        api_url = reverse(
            'hospedes:check_in_api',
            kwargs={'id': hospede.id}
        )
        response = self.client.get(
            api_url,
            data=data_hospede,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao
        # verificando se os dados do hospede sao os mesmo da response
        self.assertEqual(
            data_hospede['nome_completo'],
            response.data['hospede']['nome_completo']
        )
        self.assertEqual(
            data_hospede['email'],
            response.data['hospede']['email']
        )

    def test_check_in_api_view_will_return_200_if_action_is_check_in(self):
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url_hospede = reverse('hospedes:criar_hospede_api')
        self.make_quarto()
        # criando os dados para o hospede em JSON
        data_hospede = {
            "nome_completo": "Hospede 1 Test",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "horario_checkin": "2024-04-25",
            "horario_checkout": "2024-05-28",
            "registrado_por": "1"
        }

        response = self.client.post(
            api_url_hospede,
            data=data_hospede,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # checando se foi recebido um code 201
        # (mostrando que usuario esta logado e criou um hospede com sucesso)
        self.assertEqual(response.status_code, 201)
        # verificando se a msg de sucesso esta contida
        self.assertIn(
            'Reserva do hóspede registrada com sucesso!',
            [msg.message for msg in messages.get_messages(response.wsgi_request)])  # noqa: E501

        # com hospede criado agora é simular a criaçao de uma reserva
        api_url_reserva = reverse('hospedes:realizar_reserva_api')
        data_reserva = {
            "forma_pagamento": "TED",
            "status_reserva": "CONFIRMADO",
            "registrado_por": "1",
            "horario_checkin": "2024-04-25",
            "horario_checkout": "2024-05-28",
            "quartos": ["1"]
        }
        response_reserva = self.client.post(
            api_url_reserva,
            data=data_reserva,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao
        # checando se foi recebido um code 201
        # (mostrando que usuario esta logado e criou uma reserva para o hospede)  # noqa: E501
        self.assertEqual(response_reserva.status_code, 201)
        # checando se o status da reserva esta como "CONFIRMADO"
        self.assertEqual(
            response_reserva.data["status_reserva"],
            "CONFIRMADO"
        )

        hospede = Hospede.objects.all().first()
        api_url = reverse(
            'hospedes:check_in_api',
            kwargs={'id': hospede.id}
        )
        # Agora passar o action correto para realizar CHECK_IN
        data_checkin = {
            "id": 1,
            "nome_completo": "TEST",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "status": "AGUARDANDO_CHECKIN",
            "horario_checkin": "2024-04-25T00:00:00-03:00",
            "registrado_por": 1,
            "action": "check_in"
        }

        response = self.client.post(
            api_url,
            data=data_checkin,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao
        # checando se a msg de sucesso esta na resposta e se temos
        # status code 200
        self.assertEqual(
            response.data['message'],
            'Check-In do visitante realizado com sucesso'
        )
        self.assertEqual(response.status_code, 200)

    def test_check_in_api_view_will_return_200_if_action_is_cancelar_reserva(self):  # noqa: E501
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url_hospede = reverse('hospedes:criar_hospede_api')
        self.make_quarto()
        # criando os dados para o hospede em JSON
        data_hospede = {
            "nome_completo": "Hospede 1 Test",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "horario_checkin": "2024-04-25",
            "horario_checkout": "2024-05-28",
            "registrado_por": "1"
        }

        response = self.client.post(
            api_url_hospede,
            data=data_hospede,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # checando se foi recebido um code 201
        # (mostrando que usuario esta logado e criou um hospede com sucesso)
        self.assertEqual(response.status_code, 201)
        # verificando se a msg de sucesso esta contida
        self.assertIn(
            'Reserva do hóspede registrada com sucesso!',
            [msg.message for msg in messages.get_messages(response.wsgi_request)])  # noqa: E501

        # com hospede criado agora é simular a criaçao de uma reserva
        api_url_reserva = reverse('hospedes:realizar_reserva_api')
        data_reserva = {
            "forma_pagamento": "TED",
            "status_reserva": "CONFIRMADO",
            "registrado_por": "1",
            "horario_checkin": "2024-04-25",
            "horario_checkout": "2024-05-28",
            "quartos": ["1"]
        }
        response_reserva = self.client.post(
            api_url_reserva,
            data=data_reserva,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao
        # checando se foi recebido um code 201
        # (mostrando que usuario esta logado e criou uma reserva para o hospede)  # noqa: E501
        self.assertEqual(response_reserva.status_code, 201)
        # checando se o status da reserva esta como "CONFIRMADO"
        self.assertEqual(
            response_reserva.data["status_reserva"],
            "CONFIRMADO"
        )

        hospede = Hospede.objects.all().first()
        api_url = reverse(
            'hospedes:check_in_api',
            kwargs={'id': hospede.id}
        )
        # Agora passar o action correto para realizar CHECK_IN
        data_checkin = {
            "id": 1,
            "nome_completo": "TEST",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "status": "AGUARDANDO_CHECKIN",
            "horario_checkin": "2024-04-25T00:00:00-03:00",
            "registrado_por": 1,
            "action": "cancelar_reserva"
        }

        response = self.client.post(
            api_url,
            data=data_checkin,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao
        # checando se a msg de sucesso esta na resposta e se temos
        # status code 200
        self.assertEqual(
            response.data['message'],
            'Reserva do hóspede cancelada com sucesso'
        )
        self.assertEqual(response.status_code, 200)
