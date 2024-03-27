from django.urls import path
from . import views


app_name = 'hospedes'

urlpatterns = [
    path(
        'realizar-reserva/',
        views.RealizarReserva.as_view(),
        name='realizar_reserva'
    ),

    path(
        'hospede-info/<int:id>/check-in',
        views.check_in,
        name='check_in'
    ),

    path(
        'hospede-info/<int:id>/check-out',
        views.check_out,
        name='check_out'
    )
]
