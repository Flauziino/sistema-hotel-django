from django.urls import path
from . import views


app_name = 'hospedes'

urlpatterns = [
    path(
        'realizar-reserva/',
        views.realizar_reserva,
        name='realizar_reserva'
    ),
]
