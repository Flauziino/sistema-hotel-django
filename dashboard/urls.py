from django.urls import path
from .views import hotel_info


app_name = 'db'

urlpatterns = [
    path('', hotel_info, name="hotel_info"),
]
