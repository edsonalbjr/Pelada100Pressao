from modulos.jogadores import lista_jogadores
from itertools import zip_longest, combinations
from copy import deepcopy

# Configurações
POSICOES = ['ZAGUEIROS', 'MEIAS', 'ATACANTES']
MAPA_POSICOES = {'zagueiro': 'ZAGUEIROS', 'meia': 'MEIAS', 'atacante': 'ATACANTES'}
NUM_TIMES = 5

def encontrar_melhor_dupla(jogadores, valor_ideal):
    """Encontra a melhor dupla de jogadores cuja soma se aproxime do valor ideal"""
    melhor_dupla = None
    menor_diferenca = float('inf')
    
    for dupla in combinations(jogadores, 2):
        soma = sum(j['habilidade'] for j in dupla)
        diferenca = abs(soma - valor_ideal)
        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            melhor_dupla = dupla
    
    return melhor_dupla

# Inicializar times
times = {pos: [] for pos in POSICOES}
for jogador in lista_jogadores:
    if pos := MAPA_POSICOES.get(jogador['posicao_primaria']):
        times[pos].append(jogador)

# Ordenar por habilidade
for pos in times:
    times[pos].sort(key=lambda j: j['habilidade'], reverse=True)

# Redistribuir jogadores
for origem, destino, pos_sec in [('MEIAS', 'ZAGUEIROS', 'zagueiro'), ('ATACANTES', 'MEIAS', 'meia')]:
    candidatos = sorted([j for j in times[origem] if j['posicao_secundaria'] == pos_sec], 
                       key=lambda j: j['habilidade'], reverse=True)
    while len(times[destino]) < 10 and candidatos:
        jogador = candidatos.pop(0)
        times[destino].append(jogador)
        times[origem].remove(jogador)
        times[destino].sort(key=lambda j: j['habilidade'], reverse=True)

# Calcular somas
soma_total = sum(sum(j['habilidade'] for j in times[pos]) for pos in POSICOES)
meta_notas = soma_total / 3
somas = {pos: sum(j['habilidade'] for j in times[pos]) for pos in POSICOES}

# Imprimir resultados
print("\n" + "="*100)
print("JOGADORES POR POSIÇÃO (REDISTRIBUÍDOS)".center(100))
print("="*100)

print("\nLISTA DE JOGADORES:")
print("-"*100)
print(f"{'ZAGUEIROS':<35} {'MEIAS':<35} {'ATACANTES':<35}")
print("-"*100)

for i, row in enumerate(zip_longest(*[times[pos] for pos in POSICOES], fillvalue=None), 1):
    linha = []
    for jogador in row:
        if jogador:
            pos_sec = '-' if jogador['posicao_secundaria'] == 'nenhum' else jogador['posicao_secundaria']
            linha.append(f"{i}- {jogador['nome']} ({jogador['habilidade']}) [{pos_sec}]")
        else:
            linha.append("")
    print(f"{linha[0]:<35} {linha[1]:<35} {linha[2]}")

print("-"*100)
print(f"\nSOMA TOTAL DAS NOTAS: {soma_total:.1f} pontos")
print(f"META POR POSIÇÃO: {meta_notas:.2f} pontos (Total {soma_total:.1f} / 3 posições)")
print(f"META POR TIME (5 TIMES): {soma_total/5:.2f} pontos (Total {soma_total:.1f} / 5 times)")
print("="*100)

print("\nSOMA DAS NOTAS POR POSIÇÃO:")
print("-"*100)
for pos in POSICOES:
    diferenca = somas[pos] - meta_notas
    sinal = "+" if diferenca > 0 else ""
    print(f"{pos:<15} → {somas[pos]:>5.1f} pontos (Meta: {meta_notas:.2f}) [{sinal}{diferenca:.2f}]")
    print(f"               → {somas[pos]/5:>5.1f} pontos por time (2 jogadores)")
print("-"*100)

# Distribuir jogadores nos times
print("\nTIMES MONTADOS:")
print("="*100)

# Inicializar estrutura dos times
times_montados = {i: {'ZAGUEIROS': [], 'MEIAS': [], 'ATACANTES': [], 'total': 0} for i in range(1, NUM_TIMES + 1)}

# Distribuir jogadores para cada posição
for pos in POSICOES:
    jogadores_disponiveis = deepcopy(times[pos])
    valor_ideal = somas[pos] / NUM_TIMES
    
    # Distribuir para os primeiros N-1 times
    for time_num in range(1, NUM_TIMES):
        if len(jogadores_disponiveis) >= 2:
            dupla = encontrar_melhor_dupla(jogadores_disponiveis, valor_ideal)
            if dupla:
                times_montados[time_num][pos].extend(dupla)
                times_montados[time_num]['total'] += sum(j['habilidade'] for j in dupla)
                for jogador in dupla:
                    jogadores_disponiveis.remove(jogador)
    
    # Último time recebe os jogadores restantes
    if len(jogadores_disponiveis) == 2:
        times_montados[NUM_TIMES][pos].extend(jogadores_disponiveis)
        times_montados[NUM_TIMES]['total'] += sum(j['habilidade'] for j in jogadores_disponiveis)

# Imprimir times montados
for time_num in range(1, NUM_TIMES + 1):
    print(f"\nTIME {time_num}:")
    print("-"*50)
    print("ZAGUEIROS:")
    for i, jogador in enumerate(times_montados[time_num]['ZAGUEIROS'], 1):
        print(f"{i}. {jogador['nome']} ({jogador['habilidade']})")
    print("\nMEIAS:")
    for i, jogador in enumerate(times_montados[time_num]['MEIAS'], 1):
        print(f"{i}. {jogador['nome']} ({jogador['habilidade']})")
    print("\nATACANTES:")
    for i, jogador in enumerate(times_montados[time_num]['ATACANTES'], 1):
        print(f"{i}. {jogador['nome']} ({jogador['habilidade']})")
    print("-"*50)
    print(f"Habilidade Total: {times_montados[time_num]['total']:.1f}")
    print("="*50)