#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import json
import unicodedata
from copy import deepcopy

# Função para remover acentos e caracteres especiais
def remover_acentos(texto):
    """Remove acentos e caracteres especiais de uma string"""
    try:
        # Normaliza para forma NFKD - separa letras dos acentos
        texto_normalizado = unicodedata.normalize('NFKD', texto)
        # Remove caracteres não-ASCII
        return ''.join([c for c in texto_normalizado if not unicodedata.combining(c)])
    except:
        # Em caso de erro, retorna o texto original
        return texto

# Lista de jogadores simplificada
jogadores = [
    # ZAGUEIROS (10)
    {"nome": "Claudino", "habilidade": 4.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "nenhum"},
    {"nome": "Diego Rocha", "habilidade": 4.5, "posicao_primaria": "meia", "posicao_secundaria": "zagueiro"},
    {"nome": "Felipe Pita", "habilidade": 4.5, "posicao_primaria": "meia", "posicao_secundaria": "zagueiro"},
    {"nome": "Joao Vitor", "habilidade": 4, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Betinho", "habilidade": 3.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Leo A.", "habilidade": 3.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "nenhum"},
    {"nome": "Thiago Sultanum", "habilidade": 3.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "nenhum"},
    {"nome": "Lazaro", "habilidade": 3.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Alysson Pink", "habilidade": 3, "posicao_primaria": "zagueiro", "posicao_secundaria": "nenhum"},
    {"nome": "Sergio Falcao", "habilidade": 2.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "atacante"},
    
    # MEIAS (10)
    {"nome": "Jackson", "habilidade": 4.5, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Manga", "habilidade": 4.5, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Cadu", "habilidade": 4.5, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Kiel", "habilidade": 4, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Paulo Thiago", "habilidade": 4, "posicao_primaria": "meia", "posicao_secundaria": "zagueiro"},
    {"nome": "Thayan", "habilidade": 4, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Bidu", "habilidade": 3.5, "posicao_primaria": "meia", "posicao_secundaria": "zagueiro"},
    {"nome": "Dato", "habilidade": 3.5, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Goncalves", "habilidade": 3.5, "posicao_primaria": "meia", "posicao_secundaria": "zagueiro"},
    {"nome": "Flavio Ureia", "habilidade": 3.5, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    
    # ATACANTES (10)
    {"nome": "Bruno Pessoa", "habilidade": 4.5, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"},
    {"nome": "Marcos S.", "habilidade": 3.5, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Lucas H.", "habilidade": 3, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Nagibio", "habilidade": 3, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"},
    {"nome": "Rafa Ribeiro", "habilidade": 3, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Hiago", "habilidade": 3, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Teixa", "habilidade": 2.5, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"},
    {"nome": "Lucas S.", "habilidade": 2, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"},
    {"nome": "Thiago Alemao", "habilidade": 2, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"},
    {"nome": "Xandinho", "habilidade": 2, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"}
]

# Configurações
POSICOES = ['ZAGUEIROS', 'MEIAS', 'ATACANTES']
NUM_TIMES = 5

# Separar jogadores por posição
times = {'ZAGUEIROS': [], 'MEIAS': [], 'ATACANTES': []}
for jogador in jogadores:
    if jogador['posicao_primaria'] == 'zagueiro':
        times['ZAGUEIROS'].append(jogador)
    elif jogador['posicao_primaria'] == 'meia':
        times['MEIAS'].append(jogador)
    else:
        times['ATACANTES'].append(jogador)

# Verificar quantidade de jogadores
total_jogadores = sum(len(times[pos]) for pos in POSICOES)
min_jogadores_por_time = 2  # Mínimo de jogadores por time para cada posição

# Verificar se temos jogadores suficientes para a quantidade de times desejada
jogadores_por_posicao = {pos: len(times[pos]) for pos in POSICOES}
min_times_possiveis = min(jogadores_por_posicao[pos] // min_jogadores_por_time for pos in POSICOES)

# Ajustar o número de times se necessário
if min_times_possiveis < NUM_TIMES:
    NUM_TIMES = max(1, min_times_possiveis)
    print(f"Ajustando para {NUM_TIMES} times devido à limitação de jogadores por posição")

# Ordenar por habilidade
for pos in times:
    times[pos].sort(key=lambda j: j['habilidade'], reverse=True)

# Calcular somas
soma_total = sum(sum(j['habilidade'] for j in times[pos]) for pos in POSICOES)
meta_notas = soma_total / 3
somas = {pos: sum(j['habilidade'] for j in times[pos]) for pos in POSICOES}

print(f"\nSOMA TOTAL DAS NOTAS: {soma_total:.1f} pontos")
print(f"META POR POSICAO: {meta_notas:.2f} pontos (Total {soma_total:.1f} / 3 posicoes)")
print(f"META POR TIME (5 TIMES): {soma_total/5:.2f} pontos (Total {soma_total:.1f} / 5 times)")
print("="*80)

print("\nSOMA DAS NOTAS POR POSICAO:")
print("-"*80)
for pos in POSICOES:
    diferenca = somas[pos] - meta_notas
    sinal = "+" if diferenca > 0 else ""
    print(f"{pos:<15} -> {somas[pos]:>5.1f} pontos (Meta: {meta_notas:.2f}) [{sinal}{diferenca:.2f}]")
    print(f"               -> {somas[pos]/5:>5.1f} pontos por time (2 jogadores)")
print("-"*80)

def encontrar_dupla_balanceada(jogadores, valor_ideal):
    """Encontra uma dupla balanceada de jogadores com base na habilidade"""
    duplas_pontuadas = []
    
    for i in range(len(jogadores)):
        for j in range(i+1, len(jogadores)):
            dupla = (jogadores[i], jogadores[j])
            soma = dupla[0]['habilidade'] + dupla[1]['habilidade']
            equilibrio = abs(soma - valor_ideal)
            duplas_pontuadas.append((dupla, equilibrio, soma))
    
    # Ordenar do melhor para o pior
    duplas_pontuadas.sort(key=lambda x: x[1])
    
    # Escolher aleatoriamente entre as 3 melhores opções
    top_opcoes = min(3, len(duplas_pontuadas))
    indice = random.randint(0, top_opcoes - 1)
    return duplas_pontuadas[indice][0]

# Inicializar estrutura dos times
times_montados = {i: {'ZAGUEIROS': [], 'MEIAS': [], 'ATACANTES': [], 'total': 0} for i in range(1, NUM_TIMES + 1)}

# Lista para armazenar as duplas formadas
duplas_formadas = []

# Distribuir jogadores para cada posição
for pos in POSICOES:
    jogadores_disponiveis = deepcopy(times[pos])
    
    # Se não houver jogadores suficientes para formar duplas em todos os times,
    # distribuir individualmente
    if len(jogadores_disponiveis) < NUM_TIMES * 2:
        # Ordenar times pelo total atual (do menor para o maior)
        times_ordenados = sorted(range(1, NUM_TIMES + 1), key=lambda x: times_montados[x]['total'])
        
        # Distribuir jogadores individualmente para times com menos pontos
        for i in range(len(jogadores_disponiveis)):
            time_num = times_ordenados[i % NUM_TIMES]
            jogador = jogadores_disponiveis[i]
            times_montados[time_num][pos].append(jogador)
            times_montados[time_num]['total'] += jogador['habilidade']
    else:
        # Distribuição normal por duplas
        valor_ideal = somas[pos] / NUM_TIMES
        
        # Distribuir para todos os times
        for time_num in range(1, NUM_TIMES + 1):
            if len(jogadores_disponiveis) >= 2:
                # Usar a função que considera o histórico
                dupla = encontrar_dupla_balanceada(jogadores_disponiveis, valor_ideal)
                if dupla:
                    times_montados[time_num][pos].extend(dupla)
                    times_montados[time_num]['total'] += sum(j['habilidade'] for j in dupla)
                    for jogador in dupla:
                        jogadores_disponiveis.remove(jogador)
                    
                    # Registrar a dupla formada
                    duplas_formadas.append(dupla)
            elif len(jogadores_disponiveis) == 1:
                # Se sobrar apenas um jogador, colocá-lo no time atual
                jogador = jogadores_disponiveis[0]
                times_montados[time_num][pos].append(jogador)
                times_montados[time_num]['total'] += jogador['habilidade']
                jogadores_disponiveis.remove(jogador)

# Verificar se há jogadores restantes e distribuí-los para os times menos pontuados
jogadores_restantes = []
for pos in POSICOES:
    jogadores_restantes.extend(times[pos])

for time in times_montados.values():
    for pos in POSICOES:
        for jogador in time[pos]:
            if jogador in jogadores_restantes:
                jogadores_restantes.remove(jogador)

# Distribuir jogadores restantes (se houver) para os times com menor pontuação
if jogadores_restantes:
    print(f"\nDistribuindo {len(jogadores_restantes)} jogadores restantes...")
    
    # Ordenar times pelo total (do menor para o maior)
    times_ordenados = sorted(range(1, NUM_TIMES + 1), key=lambda x: times_montados[x]['total'])
    
    for idx, jogador in enumerate(jogadores_restantes):
        time_num = times_ordenados[idx % NUM_TIMES]
        pos = {'zagueiro': 'ZAGUEIROS', 'meia': 'MEIAS'}.get(jogador['posicao_primaria'], 'ATACANTES')
        times_montados[time_num][pos].append(jogador)
        times_montados[time_num]['total'] += jogador['habilidade']
        print(f"  Adicionando {jogador['nome']} ({jogador['habilidade']} estrelas) ao Time {time_num}")

# Imprimir times no formato original
print("\nTimes Sorteados\n")

for time_num in range(1, NUM_TIMES + 1):
    time = times_montados[time_num]
    
    # Calcular total de estrelas
    total_estrelas = time['total']
    
    # Imprimir cabeçalho do time
    print(f"--------------- Time {time_num} ---------------")
    print(f"Time {time_num} | {total_estrelas:.1f} Estrelas\n")
    
    # Imprimir jogadores
    for pos in POSICOES:
        for jogador in time[pos]:
            pos_atual = pos[:3]  # Pega as 3 primeiras letras da posição atual
            nome_limpo = remover_acentos(jogador['nome'])
            print(f"{nome_limpo} | {jogador['habilidade']} Estrelas | {pos_atual}")
    
    print() 