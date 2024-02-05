import random

# Criando a matriz de jogadores
jogadores = [
    {"nome": "Jogador1", "habilidade": 1, "adm": True, "posicao": "atacante"},
    {"nome": "Jogador2", "habilidade": 1, "adm": False, "posicao": "atacante"},
    {"nome": "Jogador3", "habilidade": 2, "adm": False, "posicao": "meia"},
    {"nome": "Jogador4", "habilidade": 2, "adm": False, "posicao": "meia"},
    {"nome": "Jogador5", "habilidade": 3, "adm": False, "posicao": "zagueiro"},
    {"nome": "Jogador6", "habilidade": 3, "adm": False, "posicao": "zagueiro"},
    {"nome": "Jogador7", "habilidade": 4, "adm": False, "posicao": "atacante"},
    {"nome": "Jogador8", "habilidade": 4, "adm": False, "posicao": "atacante"},
    {"nome": "Jogador9", "habilidade": 5, "adm": False, "posicao": "meia"},
    {"nome": "Jogador10", "habilidade": 5, "adm": True, "posicao": "meia"}
]

# Embaralhando a ordem dos jogadores aleatoriamente
random.shuffle(jogadores)

# Separando jogadores para os times
time1 = jogadores[:5]
time2 = jogadores[5:]

# Calculando a soma das habilidades para cada time
soma_habilidades_time1 = sum(jogador["habilidade"] for jogador in time1)
soma_habilidades_time2 = sum(jogador["habilidade"] for jogador in time2)

# Exibindo os times com a soma das habilidades
print("Time 1:")
for jogador in time1:
    print(jogador)

print(f"\nSoma das habilidades do Time 1: {soma_habilidades_time1}")

print("\nTime 2:")
for jogador in time2:
    print(jogador)

print(f"\nSoma das habilidades do Time 2: {soma_habilidades_time2}")
