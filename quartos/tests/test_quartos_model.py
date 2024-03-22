from django.db.utils import IntegrityError

from usuarios.tests.test_usuarios_base import BaseTestMixin, Quarto

import io
import os

from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


class QuartosModelTest(BaseTestMixin):

    def setUp(self) -> None:
        # criando uma imagem fake
        self.image_django = 'test_image.jpg'
        self.image_path = os.path.join(settings.MEDIA_ROOT, self.image_django)
        # Resolvendo o caminho absoluto se necessário
        self.image_path = os.path.abspath(self.image_path)
        self.image = Image.new('RGB', (800, 600), 'white')
        self.image.save(self.image_path, 'JPEG')

    def test_quartos_string_representation(self):
        quarto = self.make_quarto()
        self.assertEqual(
            str(quarto),
            f'Quarto: {quarto.numero_quarto} tipo: {quarto.tipo_quarto}'
        )

    def test_quartos_numero_quarto_shoud_be_unique(self):
        with self.assertRaises(IntegrityError):
            self.make_quarto()
            self.make_quarto()

    def test_quartos_tipos_quarto_field_max_length(self):
        quarto = self.make_quarto()
        self.assertEqual(
            quarto._meta.get_field('tipo_quarto').max_length,
            10
        )

    def test_quartos_tipo_quarto_is_PADRAO_by_default(self):
        quarto = Quarto.objects.create(
            numero_quarto='105',
            descricao_quarto='Harro'
        )

        self.assertEqual(
            quarto.tipo_quarto, 'PADRAO'
        )

    def test_save_method_cover_changed(self):
        image = Image.new("RGB", (100, 100), "white")
        image_bytes_io = io.BytesIO()
        image.save(image_bytes_io, format="JPEG")

        new_cover = SimpleUploadedFile(
            "new_cover.jpg",
            image_bytes_io.getvalue(),
            content_type="image/jpeg"
        )
        quarto = self.make_quarto()
        quarto.save()
        quarto.imagem = new_cover
        quarto.save()

        self.assertTrue(getattr(
            quarto, 'cover_changed', True
        ))

    def test_resize_imagem_method_is_working_right(self):
        # Criando uma instância de Quarto
        quarto = self.make_quarto()

        # adicionando uma imagem
        quarto.imagem = self.image_django
        quarto.save()

        # Carregando a imagem usando o caminho
        image_obj = Image.open(self.image_path)

        # Chamando o método resize_image() com o objeto de imagem
        quarto.resize_image(image_obj, new_width=400)

        # Verificando se a nova imagem foi salva corretamente
        self.assertTrue(os.path.exists(self.image_path))

        # Carregando a nova imagem para verificar suas dimensões
        new_image = Image.open(self.image_path)

        # Verificando se a nova imagem tem o mesmo tamanho que
        # foi passado para dentro da função
        self.assertEqual(new_image.size, (400, 300))
