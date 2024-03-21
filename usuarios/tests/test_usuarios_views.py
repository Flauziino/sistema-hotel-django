from django.test import TestCase

from django.urls import reverse, resolve

from usuarios import views


class UsuariosIndexTest(TestCase):

    # tests da view index
    def test_usuarios_index_views_function_is_correct(self):
        view = resolve(
            reverse(
                'index'
            )
        )
        self.assertIs(view.func, views.index)
