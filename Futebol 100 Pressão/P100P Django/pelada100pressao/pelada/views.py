from django.shortcuts import render
from .models import Pelada, Jogador, Estatisticas


def index(request):
    peladas = Pelada.objects.all()
    return render(request, 'index.html', {'peladas': peladas})


def perfil_jogador(request, jogador_id):
    jogador = Jogador.objects.get(id=jogador_id)
    estatisticas = Estatisticas.objects.get(jogador=jogador)
    return render(request, 'perfil_jogador.html', {'jogador': jogador, 'estatisticas': estatisticas})

# Adicione outras views conforme necessário para cadastro de peladas, jogadores, etc.
