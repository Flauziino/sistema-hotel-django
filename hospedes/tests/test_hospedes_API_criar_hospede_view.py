from django.contrib import messages
from django.urls import reverse, resolve

from hospedes.views import api
from .test_hospedes_API_base import APIBaseTestMixin


class TestCriarHospedeAPIView(APIBaseTestMixin):
    def test_criar_hospede_api_view_function_is_correct(self):
        view = resolve(
            reverse('hospedes:criar_hospede_api')
        )
        self.assertIs(view.func.view_class, api.CriarHospedeAPIView)

    def test_criar_hospede_api_view_returns_code_401_if_not_authenticated(self):  # noqa: E501
        api_url = reverse('hospedes:criar_hospede_api')
        response = self.client.post(
            api_url,
            data={}
        )
        self.assertEqual(response.status_code, 401)

    def test_criar_hospede_api_view_authenticated_user_can_create_a_hospede(self):  # noqa: E501
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url = reverse('hospedes:criar_hospede_api')

        # criando os dados para o hospede em JSON
        data = {
            "nome_completo": "Hospede 1 Test",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "horario_checkin": "2024-04-25",
            "horario_checkout": "2024-05-08",
            "registrado_por": "1"
        }

        response = self.client.post(
            api_url,
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

    def test_criar_hospede_api_view_authenticated_fails_to_create_a_hospede(self):  # noqa: E501
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url = reverse('hospedes:criar_hospede_api')

        # criando os dados para o hospede em JSON
        # esperando falhar
        data = {
        }

        response = self.client.post(
            api_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # checando se foi recebido um code 400
        # (mostrando que o usuario nao conseguiu criar o hospede)
        self.assertEqual(response.status_code, 400)
        # verificando se contem a msg de erro
        self.assertIn(
            'Erro ao criar hóspede. Por favor, verifique os dados.',
            [msg.message for msg in messages.get_messages(response.wsgi_request)])  # noqa: E501

    def test_criar_hospede_api_view_receive_wrong_credentials_and_fails_to_create_hospede(self):  # noqa: E501
        api_url = reverse('hospedes:criar_hospede_api')

        # simulando um usuario invalido
        user = self.get_user(
            username='username',
            password='password'
        )

        self.make_porteiro(usuario=user)

        # pegando credenciais erradas
        response = self.client.post(
            reverse('hospedes:token_obtain_pair'), data={'username': 'fail',
                                                         'password': 'fail'}
        )
        fake_access = response.data.get('access')

        # criando os dados para o hospede em JSON
        # esperando falhar pois o usuario ira passar as credenciais erradas
        # e nao estara logado no sistema
        data = {
            "nome_completo": "Hospede 1 Test",
            "telefone": "35991445522",
            "cpf": "11122222456",
            "email": "seuemail@email.com",
            "horario_checkin": "2024-04-25",
            "horario_checkout": "2024-05-08",
            "registrado_por": "1"
        }

        response = self.client.post(
            api_url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {fake_access}'
        )

        # checando se foi recebido um code 401
        self.assertEqual(response.status_code, 401)

    def test_criar_hospede_api_view_will_receive_code_405_if_method_is_not_post(self):  # noqa: E501
        # pegando um usuario
        auth_data = self.get_auth_data()
        # pegando seu acesso com jwt token
        jwt_access = auth_data.get('jwt_access_token')

        api_url = reverse(
            'hospedes:criar_hospede_api'
        )

        response = self.client.get(
            api_url,
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'   # passando o acesso do
        )  # usuario para a autorizaçao

        # verificando se recebe um code 405 (método nao permitido)
        # pois essa view só recebe "POST"
        self.assertEqual(response.status_code, 405)
