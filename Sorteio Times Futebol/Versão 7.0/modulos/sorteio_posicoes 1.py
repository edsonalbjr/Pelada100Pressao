from modulos.jogadores import lista_jogadores
from operator import itemgetter
from itertools import zip_longest

def formatar_jogador(num, jogador):
    """Formata a string do jogador com número, nome, habilidade e posição secundária"""
    pos_sec = '-' if jogador['posicao_secundaria'] == 'nenhum' else jogador['posicao_secundaria']
    return f"{num}- {jogador['nome']} ({jogador['habilidade']}) [{pos_sec}]"

def soma_habilidades(jogadores):
    """Calcula a soma das habilidades de um grupo de jogadores"""
    return sum(j['habilidade'] for j in jogadores)

def redistribuir_jogadores(times, meta_notas):
    """Redistribui jogadores para equilibrar as notas entre as posições"""
    # Encontrar jogadores que podem ser movidos
    jogadores_para_zagueiro = [j for j in times['MEIAS'] if j['posicao_secundaria'] == 'zagueiro']
    jogadores_para_meia = [j for j in times['ATACANTES'] if j['posicao_secundaria'] == 'meia']
    
    # Ordenar por habilidade (maior para menor)
    jogadores_para_zagueiro.sort(key=itemgetter('habilidade'), reverse=True)
    jogadores_para_meia.sort(key=itemgetter('habilidade'), reverse=True)
    
    # Mover jogadores para zagueiro
    while len(times['ZAGUEIROS']) < 10 and jogadores_para_zagueiro:
        jogador = jogadores_para_zagueiro.pop(0)
        times['ZAGUEIROS'].append(jogador)
        times['MEIAS'].remove(jogador)
    
    # Mover jogadores para meia
    while len(times['MEIAS']) < 10 and jogadores_para_meia:
        jogador = jogadores_para_meia.pop(0)
        times['MEIAS'].append(jogador)
        times['ATACANTES'].remove(jogador)
    
    # Reordenar as listas
    for pos in times:
        times[pos].sort(key=itemgetter('habilidade'), reverse=True)
    
    return times

# Mapeamento de posições
POSICOES = ['ZAGUEIROS', 'MEIAS', 'ATACANTES']
MAPA_POSICOES = {'zagueiro': 'ZAGUEIROS', 'meia': 'MEIAS', 'atacante': 'ATACANTES'}

# Organizar jogadores por posição
times = {pos: [] for pos in POSICOES}
for jogador in lista_jogadores:
    pos_principal = MAPA_POSICOES.get(jogador['posicao_primaria'])
    if pos_principal:
        times[pos_principal].append(jogador)

# Ordenar cada lista por habilidade
for jogadores in times.values():
    jogadores.sort(key=itemgetter('habilidade'), reverse=True)

# Calcular soma total e meta
somas = {pos: soma_habilidades(times[pos]) for pos in POSICOES}
soma_total = sum(somas.values())
meta_notas = soma_total / 3

# Redistribuir jogadores
times = redistribuir_jogadores(times, meta_notas)

# Recalcular somas após redistribuição
somas = {pos: soma_habilidades(times[pos]) for pos in POSICOES}
soma_total = sum(somas.values())

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
        linha.append(formatar_jogador(i, jogador) if jogador else "")
    print(f"{linha[0]:<35} {linha[1]:<35} {linha[2]}")

print("-"*100)
print(f"\nSOMA TOTAL DAS NOTAS: {soma_total:.1f} pontos")
print(f"META POR POSIÇÃO: {meta_notas:.2f} pontos (Total {soma_total:.1f} / 3 posições)")
print("="*100)

print("\nSOMA DAS NOTAS POR POSIÇÃO:")
print("-"*100)
for pos in POSICOES:
    diferenca = somas[pos] - meta_notas
    sinal = "+" if diferenca > 0 else ""
    print(f"{pos:<15} → {somas[pos]:>5.1f} pontos (Meta: {meta_notas:.2f}) [{sinal}{diferenca:.2f}]")
print("-"*100)