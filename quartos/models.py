import os
from django.db import models
from PIL import Image
from django.conf import settings


class Quarto(models.Model):

    QUARTOS_CHOICE = [
        ('SIMPLES', 'Quarto simples'),
        ('PADRAO', 'Quarto padrão do hotel'),
        ('LUXO', 'Quarto luxuoso')
    ]

    numero_quarto = models.PositiveSmallIntegerField(
        verbose_name="Número do quarto",
        unique=True
    )

    tipo_quarto = models.CharField(
        verbose_name='Tipo de quarto para hospedagem',
        choices=QUARTOS_CHOICE,
        max_length=10,
        default='PADRAO'
    )

    imagem = models.ImageField(
        upload_to='quarto_img/',
        blank=True,
        null=True
    )

    descricao_quarto = models.TextField()

    @staticmethod
    def resize_image(img, new_width=800):
        if isinstance(img, Image.Image):
            img_full_path = os.path.join(settings.MEDIA_ROOT, img.filename)
        else:
            img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)

        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return

        new_height = round(
            (new_width * original_height) / original_width
        )

        new_img = img_pil.resize(
            (new_width, new_height), Image.LANCZOS
        )

        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_img_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_img_size)

    class Meta:
        verbose_name = 'Quarto'
        verbose_name_plural = 'Quartos'
        db_table = 'quarto'

    def __str__(self):
        return f'Quarto: {self.numero_quarto} tipo: {self.tipo_quarto}'
