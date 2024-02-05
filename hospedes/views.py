from django.shortcuts import render
from django.http import HttpResponse


def registrar_hospede(request):
    return HttpResponse(
        'Ola Hospede'
    )
