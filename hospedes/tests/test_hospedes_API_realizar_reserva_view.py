from django.contrib import messages
from django.urls import reverse, resolve

from hospedes.views import api
from .test_hospedes_API_base import APIBaseTestMixin


class TestRealizarReservaAPIView(APIBaseTestMixin):
    def test_realizar_reserva_api_view_function_is_correct(self):
        view = resolve(
            reverse('hospedes:realizar_reserva_api')
        )

        self.assertIs(view.func.view_class, api.RealizarReservaAPIView)

    def test_realizar_reserva_api_view_return_code_401_if_not_logged(self):
        api_url = reverse(
            'hospedes:realizar_reserva_api'
        )

        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 401)

    def test_realizar_reserva_api_will_receive_code_405_if_method_is_not_post(self):  # noqa: E501
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url = reverse(
            'hospedes:realizar_reserva_api'
        )

        response = self.client.get(
            api_url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # verificando se recebe um code 405 (método nao permitido)
        # pois essa view só recebe "POST"
        self.assertEqual(response.status_code, 405)

    def test_realizar_reserva_api_view_authenticated_user_can_realizar_reserva(self):  # noqa: E501
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url_hospede = reverse('hospedes:criar_hospede_api')

        self.make_quarto()
        # criando os dados para o hospede em JSON
        data = {
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
            data=data,
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

    def test_realizar_reserva_api_view_receive_a_wrong_date_and_fail_to_create_reserva_code_400(self):  # noqa: E501
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url_hospede = reverse('hospedes:criar_hospede_api')

        # criando os dados para o hospede em JSON
        data = {
            "nome_completo": "Hospede 1 Test",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "horario_checkin": "2024-03-25",
            "horario_checkout": "2024-03-28",
            "registrado_por": "1"
        }

        response = self.client.post(
            api_url_hospede,
            data=data,
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
            "horario_checkin": "2024-03-25",
            "horario_checkout": "2024-03-28",
            "quartos": ["1"]
        }

        response_reserva = self.client.post(
            api_url_reserva,
            data=data_reserva,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # checando se foi recebido um code 400
        # (mostrando que usuario esta logado mas falhou em criar a reserva)  # noqa: E501
        self.assertEqual(response_reserva.status_code, 400)

        # checando se a msg de error esta visivel
        self.assertEqual(
            response_reserva.data["error"],
            'Data incorreta'
        )

    def test_realizar_reserva_api_view_receive_a_occupied_quarto_and_fail_to_create_reserva_code_400(self):  # noqa: E501
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url_hospede = reverse('hospedes:criar_hospede_api')

        # criando os dados para o hospede em JSON
        data = {
            "nome_completo": "Hospede 1 Test",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "horario_checkin": "2024-05-25T00:00:00",
            "horario_checkout": "2024-05-28T00:00:00",
            "registrado_por": "1"
        }

        response = self.client.post(
            api_url_hospede,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # checando se foi recebido um code 201
        # (mostrando que usuario esta logado e criou um hospede com sucesso)
        self.assertEqual(response.status_code, 201)

        # criando o quarto
        self.make_quarto()
        # com hospede criado agora é simular a criaçao de uma reserva
        api_url_reserva = reverse('hospedes:realizar_reserva_api')
        data_reserva = {
            "forma_pagamento": "TED",
            "status_reserva": "CONFIRMADO",
            "horario_checkin": "2024-05-25T00:00:00",
            "horario_checkout": "2024-05-28T00:00:00",
            "quartos": ["1"]
        }

        response_reserva = self.client.post(
            api_url_reserva,
            data=data_reserva,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        self.assertEqual(response_reserva.status_code, 201)

        # criando outro hospede para tentar realizar uma reserva pra ele com
        # um quarto ja ocupado para o periodo de tempo selecionado
        hospede_2 = {
            "nome_completo": "Hospede 2 Test",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "horario_checkin": "2024-05-25T00:00:00",
            "horario_checkout": "2024-05-28T00:00:00",
            "registrado_por": "1"
        }

        response_2 = self.client.post(
            api_url_hospede,
            data=hospede_2,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # checando se foi recebido um code 201
        self.assertEqual(response_2.status_code, 201)

        # com hospede criado agora é simular a criaçao de uma reserva
        # para um quarto ja ocupado
        api_url_reserva = reverse('hospedes:realizar_reserva_api')
        reserva_2 = {
            "forma_pagamento": "TED",
            "status_reserva": "CONFIRMADO",
            "horario_checkin": "2024-05-25T00:00:00",
            "horario_checkout": "2024-05-28T00:00:00",
            "quartos": ["1"]
        }

        response_reserva_2 = self.client.post(
            api_url_reserva,
            data=reserva_2,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # VERDADEIRO TESTE, ESPERA-SE UM CODE 400
        self.assertEqual(response_reserva_2.status_code, 400)
        self.assertEqual(
            response_reserva_2.data["error"],
            'O quarto já está ocupado!'
        )

    def test_realizar_reserva_api_view_receive_invalid_data_return_bad_request_code_400(self):  # noqa: E501
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url_hospede = reverse('hospedes:criar_hospede_api')

        # criando um quarto
        self.make_quarto()
        # criando os dados para o hospede em JSON
        data = {
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
            data=data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # checando se foi recebido um code 201
        # (mostrando que usuario esta logado e criou um hospede com sucesso)
        self.assertEqual(response.status_code, 201)
        # verificando se a msg de sucesso esta contida
        self.assertIn(
            'Reserva do hóspede registrada com sucesso!',
            [msg.message for msg in messages.get_messages(response.wsgi_request)])  # noqa: E501

        # com hospede criado agora é simular o envio de um formato invalid
        # para dentro do serializer
        api_url_reserva = reverse('hospedes:realizar_reserva_api')
        data_reserva = {
            "forma_pagamento": "TEDi",
            "status_reserva": "CONFIRMADAA",
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
        print(response_reserva.content)
        # checando se foi recebido um code 400
        self.assertEqual(response_reserva.status_code, 400)

        # checando se o erro esperado esta condigo
        self.assertEqual(
            response_reserva.data["error"],
            'Formulario invalido'
        )
