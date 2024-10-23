from django.shortcuts import render
from django.http import HttpResponse

def ultra_subdomain_view(request, path=None):
    # Retornar '<h1>Olá Mundo!</h1>' se não houver subdomínio
    return HttpResponse('<h1>Olá Mundo!</h1>')
