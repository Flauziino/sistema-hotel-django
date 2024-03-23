from django.test import TestCase
from django.urls import reverse


class UsuariosURLsTest(TestCase):

    # teste de URLS
    def test_usuarios_index_url_is_correct(self):
        url = reverse('index')
        self.assertEqual(url, '/')
