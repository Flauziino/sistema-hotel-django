# Generated by Django 4.2.11 on 2024-03-28 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_usuario_groups_alter_usuario_user_permissions'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
