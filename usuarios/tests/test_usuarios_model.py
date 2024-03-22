from .test_usuarios_base import BaseTestMixin


class UsuariosModelTest(BaseTestMixin):
    def test_usuario_string_representation(self):
        user = self.get_user()
        self.assertEqual(
            str(user), user.username
        )
