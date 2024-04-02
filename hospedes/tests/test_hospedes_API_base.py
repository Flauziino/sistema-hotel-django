from rest_framework import test

from django.urls import reverse

from usuarios.tests.test_usuarios_base import BaseTestMixin


class APIBaseTestMixin(test.APITestCase, BaseTestMixin):
    def get_auth_data(self, username='user', password='password'):
        user = self.get_user(
            username=username,
            password=password
        )

        data = {
            'username': username,
            'password': password
        }

        porteiro = self.make_porteiro(usuario=user)

        response = self.client.post(
            reverse('hospedes:token_obtain_pair'), data={**data}
        )
        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'porteiro': porteiro,
            'data': data
        }
