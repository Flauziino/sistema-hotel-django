from django.urls import path
from .views import site, api

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


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
    ),

    # API #
    path(
        'index-api',
        api.IndexAPIView.as_view(),
        name='index_api'
    ),
    path(
        'criar-hospede-api',
        api.CriarHospedeAPIView.as_view(),
        name='criar_hospede_api'
    ),
    path(
        'realizar-reserva-api',
        api.RealizarReservaAPIView.as_view(),
        name='realizar_reserva_api'
    ),
    path(
        'hospede-info-api/<int:id>/check-in',
        api.CheckInAPIView.as_view(),
        name='check_in_api'
    ),
    path(
        'hospede-info-api/<int:id>/check-out',
        api.CheckOutAPIView.as_view(),
        name='check_out_api'
    ),

    # JWT #
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
    # Por último
]
