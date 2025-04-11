from modules.jogadores import lista_jogadores
from itertools import zip_longest, combinations
from copy import deepcopy
import random

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

def imprimir_lista_jogadores(times, titulo):
    """Imprime a lista de jogadores formatada"""
    print("\n" + "="*100)
    print(titulo.center(100))
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

def redistribuir_jogadores(times):
    """Redistribui jogadores mantendo o equilíbrio de habilidades"""
    # Análise inicial da quantidade de jogadores
    print("\nANÁLISE INICIAL DA DISTRIBUIÇÃO:")
    print("-"*50)
    for pos in POSICOES:
        qtd = len(times[pos])
        print(f"{pos}: {qtd} jogadores")
    print("-"*50)
    
    # Mapeamento reverso para posições secundárias
    posicoes_secundarias_reverso = {
        'zagueiro': 'ZAGUEIROS',
        'meia': 'MEIAS',
        'atacante': 'ATACANTES'
    }
    
    def encontrar_jogadores_para_mover(origem, posicao_destino):
        """Encontra jogadores que podem ser movidos de uma posição para outra"""
        jogadores = []
        for jogador in times[origem]:
            if jogador['posicao_secundaria'] == posicao_destino:
                jogadores.append(jogador)
        return jogadores
    
    def mover_jogador(origem, destino, jogador, is_coringa=False):
        """Move um jogador de uma posição para outra"""
        times[destino].append(jogador)
        times[origem].remove(jogador)
        # Reordenar após mover
        times[destino].sort(key=lambda j: j['habilidade'], reverse=True)
        times[origem].sort(key=lambda j: j['habilidade'], reverse=True)
        # Mostrar mensagem se for coringa
        if is_coringa:
            print(f"\nUSANDO CORINGA: {jogador['nome']} ({jogador['habilidade']}) movido de {origem} para {destino}")
    
    def encontrar_coringa(origem, destino):
        """Encontra o melhor jogador para ser coringa"""
        # Primeiro, encontrar jogadores sem posição secundária
        jogadores_sem_secundaria = [j for j in times[origem] if j['posicao_secundaria'] == 'nenhum']
        if not jogadores_sem_secundaria:
            return None
            
        # Encontrar a maior nota entre os jogadores sem posição secundária
        maior_nota = max(j['habilidade'] for j in jogadores_sem_secundaria)
        # Pegar todos os jogadores com essa nota
        coringas = [j for j in jogadores_sem_secundaria if j['habilidade'] == maior_nota]
        return coringas[0] if coringas else None
    
    # Loop principal de redistribuição
    while True:
        # Verificar quantos jogadores cada posição tem
        contagem = {pos: len(times[pos]) for pos in POSICOES}
        
        # Se todas as posições tiverem 10 jogadores, parar
        if all(qtd == 10 for qtd in contagem.values()):
            break
            
        # Encontrar posições que precisam de jogadores
        posicoes_necessitadas = [pos for pos, qtd in contagem.items() if qtd < 10]
        posicoes_sobrando = [pos for pos, qtd in contagem.items() if qtd > 10]
        
        # Se não houver posições para ajustar, parar
        if not posicoes_necessitadas or not posicoes_sobrando:
            break
            
        # Tentar mover jogadores
        movimento_realizado = False
        
        # 1. Tentar mover usando posições secundárias
        for origem in posicoes_sobrando:
            for destino in posicoes_necessitadas:
                # Encontrar jogadores que podem ser movidos
                jogadores = encontrar_jogadores_para_mover(origem, destino.lower())
                if jogadores:
                    # Ordenar por habilidade
                    jogadores.sort(key=lambda j: j['habilidade'], reverse=True)
                    # Mover o melhor jogador
                    mover_jogador(origem, destino, jogadores[0])
                    movimento_realizado = True
                    break
            if movimento_realizado:
                break
        
        # 2. Se não conseguiu mover usando posições secundárias, tentar usar coringa
        if not movimento_realizado:
            for origem in posicoes_sobrando:
                for destino in posicoes_necessitadas:
                    # Encontrar coringa
                    coringa = encontrar_coringa(origem, destino)
                    if coringa:
                        mover_jogador(origem, destino, coringa, is_coringa=True)
                        movimento_realizado = True
                        break
                if movimento_realizado:
                    break
                
        # Se não conseguiu mover de nenhuma forma, parar
        if not movimento_realizado:
            break
    
    # Análise final da quantidade de jogadores
    print("\nANÁLISE FINAL DA DISTRIBUIÇÃO:")
    print("-"*50)
    for pos in POSICOES:
        qtd = len(times[pos])
        print(f"{pos}: {qtd} jogadores")
    print("-"*50)
    
    return times

# Inicializar times
times = {pos: [] for pos in POSICOES}
for jogador in lista_jogadores:
    if pos := MAPA_POSICOES.get(jogador['posicao_primaria']):
        times[pos].append(jogador)

# Ordenar por habilidade
for pos in times:
    times[pos].sort(key=lambda j: j['habilidade'], reverse=True)

# Imprimir lista inicial
imprimir_lista_jogadores(times, "JOGADORES POR POSIÇÃO (INICIAL)")

# Redistribuir jogadores
times = redistribuir_jogadores(times)

# Imprimir lista após redistribuição
imprimir_lista_jogadores(times, "JOGADORES POR POSIÇÃO (APÓS REDISTRIBUIÇÃO)")

# Calcular somas
soma_total = sum(sum(j['habilidade'] for j in times[pos]) for pos in POSICOES)
meta_notas = soma_total / 3
somas = {pos: sum(j['habilidade'] for j in times[pos]) for pos in POSICOES}

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

# Embaralhar a ordem dos times
ordem_times = list(range(1, NUM_TIMES + 1))
random.shuffle(ordem_times)

# Criar um dicionário para mapear a nova ordem
mapeamento = {i+1: ordem_times[i] for i in range(NUM_TIMES)}

# Imprimir times no novo formato
def imprimir_times_novo_formato(times_montados):
    """Imprime os times no novo formato"""
    print("\nTimes Sorteados\n")
    
    for time_num in range(1, NUM_TIMES + 1):
        time = times_montados[time_num]
        
        # Calcular total de estrelas
        total_estrelas = time['total']
        
        # Imprimir cabeçalho do time
        print(f"{'---------------':^15} Time {time_num} {'---------------':^15}")
        print(f"Time {time_num} | {total_estrelas:.1f} Estrelas\n")
        
        # Imprimir jogadores
        for pos in POSICOES:
            for jogador in time[pos]:
                pos_atual = pos[:3]  # Pega as 3 primeiras letras da posição atual
                print(f"{jogador['nome']} | {jogador['habilidade']} Estrelas | {pos_atual}")
        
        print()

imprimir_times_novo_formato(times_montados)