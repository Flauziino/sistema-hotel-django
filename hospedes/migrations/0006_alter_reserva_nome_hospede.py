# Generated by Django 5.0.1 on 2024-02-05 20:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospedes', '0005_alter_reserva_horario_checkout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='nome_hospede',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospedes.hospede'),
        ),
    ]
