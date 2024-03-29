from django.urls import path
from .views import site


app_name = 'hospedes'

urlpatterns = [
    path(
        'realizar-reserva/',
        site.RealizarReservaView.as_view(),
        name='realizar_reserva'
    ),

    path(
        'hospede-info/<int:id>/check-in',
        site.CheckInView.as_view(),
        name='check_in'
    ),

    path(
        'hospede-info/<int:id>/check-out',
        site.CheckOutView.as_view(),
        name='check_out'
    )
]
