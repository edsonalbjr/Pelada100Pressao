from modulos.jogadores import lista_jogadores
from operator import itemgetter
from itertools import zip_longest

# Posições e mapeamento
POSICOES = ['ZAGUEIROS', 'MEIAS', 'ATACANTES']
MAPA_POSICOES = {'zagueiro': 'ZAGUEIROS', 'meia': 'MEIAS', 'atacante': 'ATACANTES'}

# Distribuir jogadores por posição
times = {pos: [] for pos in POSICOES}
for jogador in lista_jogadores:
    pos = MAPA_POSICOES.get(jogador['posicao_primaria'])
    if pos:
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
    
    # Reordenar posições
    times[destino].sort(key=lambda j: j['habilidade'], reverse=True)

# Calcular somas e meta
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

# Imprimir jogadores em colunas
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

# Exibição dos times vazios
print("\nTIMES MONTADOS:")
print("="*100)

for time_num in range(1, 6):
    print(f"\nTIME {time_num}:")
    print("-"*50)
    print("ZAGUEIROS:")
    print("1. _______________________")
    print("2. _______________________")
    print("\nMEIAS:")
    print("1. _______________________")
    print("2. _______________________")
    print("\nATACANTES:")
    print("1. _______________________")
    print("2. _______________________")
    print("-"*50)
    print(f"Habilidade Total: 0.0")
    print("="*50)