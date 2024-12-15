import random

# Dados fictícios dos jogadores
data = [
    # Jogadores Defensivos
    {"Nome": "Jogador D1", "Habilidade": 9.0, "Posicao": "Zagueiro", "Fisico": "Força", "Pe": "Destro", "Estilo": "Estratégico"},
    {"Nome": "Jogador D2", "Habilidade": 8.8, "Posicao": "Zagueiro", "Fisico": "Equilíbrio", "Pe": "Canhoto", "Estilo": "Técnico"},
    {"Nome": "Jogador D3", "Habilidade": 7.5, "Posicao": "Zagueiro", "Fisico": "Força", "Pe": "Destro", "Estilo": "Estratégico"},
    {"Nome": "Jogador D4", "Habilidade": 6.8, "Posicao": "Alas", "Fisico": "Velocista", "Pe": "Destro", "Estilo": "Técnico"},
    {"Nome": "Jogador D5", "Habilidade": 5.5, "Posicao": "Alas", "Fisico": "Agilidade", "Pe": "Canhoto", "Estilo": "Velocista"},
    {"Nome": "Jogador D6", "Habilidade": 4.2, "Posicao": "Zagueiro", "Fisico": "Força", "Pe": "Destro", "Estilo": "Estratégico"},

    # Jogadores Meias
    {"Nome": "Jogador M1", "Habilidade": 9.9, "Posicao": "Meia", "Fisico": "Equilíbrio", "Pe": "Destro", "Estilo": "Estratégico"},
    {"Nome": "Jogador M2", "Habilidade": 8.5, "Posicao": "Volante", "Fisico": "Força", "Pe": "Canhoto", "Estilo": "Técnico"},
    {"Nome": "Jogador M3", "Habilidade": 7.9, "Posicao": "Meia", "Fisico": "Agilidade", "Pe": "Destro", "Estilo": "Velocista"},
    {"Nome": "Jogador M4", "Habilidade": 6.3, "Posicao": "Meia", "Fisico": "Equilíbrio", "Pe": "Destro", "Estilo": "Estratégico"},
    {"Nome": "Jogador M5", "Habilidade": 5.7, "Posicao": "Volante", "Fisico": "Força", "Pe": "Canhoto", "Estilo": "Técnico"},
    {"Nome": "Jogador M6", "Habilidade": 4.2, "Posicao": "Meia", "Fisico": "Agilidade", "Pe": "Destro", "Estilo": "Velocista"},

    # Jogadores Atacantes
    {"Nome": "Jogador A1", "Habilidade": 9.5, "Posicao": "Fixo", "Fisico": "Força", "Pe": "Destro", "Estilo": "Técnico"},
    {"Nome": "Jogador A2", "Habilidade": 8.0, "Posicao": "Ponta", "Fisico": "Agilidade", "Pe": "Canhoto", "Estilo": "Velocista"},
    {"Nome": "Jogador A3", "Habilidade": 7.7, "Posicao": "Ponta", "Fisico": "Velocista", "Pe": "Destro", "Estilo": "Técnico"},
    {"Nome": "Jogador A4", "Habilidade": 6.8, "Posicao": "Ponta", "Fisico": "Velocista", "Pe": "Canhoto", "Estilo": "Velocista"},
    {"Nome": "Jogador A5", "Habilidade": 5.2, "Posicao": "Fixo", "Fisico": "Força", "Pe": "Destro", "Estilo": "Estratégico"},
    {"Nome": "Jogador A6", "Habilidade": 4.8, "Posicao": "Fixo", "Fisico": "Força", "Pe": "Destro", "Estilo": "Técnico"}
]

# Configuração inicial
num_times = 2

# 1. Separar jogadores por posições
posicoes = {"Defensivo": [], "Meia": [], "Ataque": []}
for jogador in data:
    if jogador["Posicao"] in ["Zagueiro", "Alas"]:
        posicoes["Defensivo"].append(jogador)
    elif jogador["Posicao"] in ["Volante", "Meia"]:
        posicoes["Meia"].append(jogador)
    elif jogador["Posicao"] in ["Fixo", "Ponta"]:
        posicoes["Ataque"].append(jogador)

# 2. Inicializar os times
teams = {f"Time {i + 1}": [] for i in range(num_times)}

# 3. Rodízio para distribuir jogadores
for posicao, jogadores in posicoes.items():
    jogadores.sort(key=lambda x: x["Habilidade"], reverse=True)
    for i, jogador in enumerate(jogadores):
        team_name = f"Time {(i % num_times) + 1}"
        teams[team_name].append(jogador)

# 4. Ordenar jogadores dentro de cada time por habilidade
for team in teams:
    teams[team].sort(key=lambda x: x["Habilidade"], reverse=True)

# 5. Mostrar os times
for team, players in teams.items():
    print(f"\n{team}:")
    for player in players:
        print(f"  - {player['Nome']} (Habilidade: {player['Habilidade']}, Posição: {player['Posicao']}, Físico: {player['Fisico']}, Pé: {player['Pe']}, Estilo: {player['Estilo']})")
