from django.urls import path
from . import views


app_name = 'hospedes'

urlpatterns = [
    path(
        'registrar-hospede/',
        views.registrar_hospede,
        name='registrar_hospede'
    ),
]
