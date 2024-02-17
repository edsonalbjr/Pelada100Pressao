# myapp/views.py
from django.shortcuts import render
from .models import Jogador  # Se você tiver um modelo para Jogador

def exibir_times(request):
    # Substitua pela lógica de criação de times e jogadores
    jogadores = [
    {"nome": "Albert", "habilidade": 5, "adm": True, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Betinho", "habilidade": 4, "adm": True, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Bidu", "habilidade": 4, "adm": False, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Bruno Pessoa", "habilidade": 3.5, "adm": False, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Dato", "habilidade": 4, "adm": False, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Diego", "habilidade": 4, "adm": False, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Eduardo", "habilidade": 4, "adm": False, "posicao_primaria": "zagueiro", "posicao_secundaria": "atacante"},
    {"nome": "Eric", "habilidade": 3.5, "adm": True, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Flávio", "habilidade": 3.5, "adm": False, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Henrique Silva", "habilidade": 4, "adm": False, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Kiel", "habilidade": 5, "adm": False, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Lucas Henrique", "habilidade": 3, "adm": False, "posicao_primaria": "atacante", "posicao_secundaria": None},
    {"nome": "Lucas Silveira", "habilidade": 1, "adm": False, "posicao_primaria": "atacante", "posicao_secundaria": None},
    {"nome": "Marcelinho", "habilidade": 4, "adm": False, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Matheus Ureia", "habilidade": 4, "adm": False, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Nicláudio Mello", "habilidade": 2.5, "adm": False, "posicao_primaria": "atacante", "posicao_secundaria": None},
    {"nome": "Raphael Borges", "habilidade": 4, "adm": False, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Teixa", "habilidade": 2.5, "adm": False, "posicao_primaria": "atacante", "posicao_secundaria": "zagueiro"},
    {"nome": "Thiago Alemão", "habilidade": 1.5, "adm": False, "posicao_primaria": "atacante", "posicao_secundaria": None},
    {"nome": "Vinícius", "habilidade": 5, "adm": False, "posicao_primaria": "atacante", "posicao_secundaria": "zagueiro"},
    {"nome": "Jackson", "habilidade": 4, "adm": False, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Sergio Falção", "habilidade": 2.5, "adm": False, "posicao_primaria": "zagueiro", "posicao_secundaria": "atacante"},
    {"nome": "Léo A.", "habilidade": 3, "adm": False, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Winnicius C.", "habilidade": 5, "adm": False, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Alysson Pink", "habilidade": 3, "adm": False, "posicao_primaria": "zagueiro", "posicao_secundaria": None}
]

    # Se você não tiver um modelo, substitua pela lista de times
    times = criar_times(jogadores, num_times)
    
    # Trocar aleatoriamente os times
    random.shuffle(times)
    
    # Trocar aleatoriamente os jogadores dentro de cada time
    for time in times:
        random.shuffle(time)
    
    context = {'times': times}
    return render(request, 'myapp/times.html', context)
