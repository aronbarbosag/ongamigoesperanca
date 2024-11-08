from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    return render(request, "app/index.html", {"idBody": " "})


def sobre(request):
    return render(request, "app/sobre.html", {"idBody": "sobre"})


def transparencia(request):
    return render(request, "app/transparencia.html", {"idBody": "transparencia"})


def voluntariado(request):
    return render(request, "app/voluntariado.html", {"idBody": "voluntariado"})


def contato(request):
    return render(request, "app/contato.html", {"idBody": "contato"})


def doacao(request):
    return render(request, "app/doacao.html", {"idBody": "doacao"})


def eventos(request):
    return render(request, "app/eventos.html", {"idBody": "eventos"})


def area_restrita(request):
    return render(request, "app/area-restrita.html", {"idBody": "area-restrita"})
