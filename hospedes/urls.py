from django.urls import path
from . import views


app_name = 'hospedes'

urlpatterns = [
    path(
        'realizar-reserva/',
        views.RealizarReservaView.as_view(),
        name='realizar_reserva'
    ),

    path(
        'hospede-info/<int:id>/check-in',
        views.CheckInView.as_view(),
        name='check_in'
    ),

    path(
        'hospede-info/<int:id>/check-out',
        views.check_out,
        name='check_out'
    )
]
