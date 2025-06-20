#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.jogadores import lista_jogadores
from itertools import zip_longest, combinations
from copy import deepcopy
import random
import json
import os
import unicodedata  # Para lidar com acentos

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

# Configurações
POSICOES = ['ZAGUEIROS', 'MEIAS', 'ATACANTES']
MAPA_POSICOES = {'zagueiro': 'ZAGUEIROS', 'meia': 'MEIAS', 'atacante': 'ATACANTES'}
NUM_TIMES = 5
HISTORICO_ARQUIVO = "historico_duplas.json"

def carregar_historico():
    """Carrega o histórico de duplas anteriores"""
    try:
        with open(HISTORICO_ARQUIVO, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"duplas": []}

def salvar_historico(duplas_novas):
    """Salva o histórico atualizado de duplas"""
    historico = carregar_historico()
    
    # Adicionar novas duplas
    for dupla in duplas_novas:
        nomes_dupla = (dupla[0]['nome'], dupla[1]['nome'])
        historico["duplas"].append(list(nomes_dupla))
    
    # Manter apenas as últimas 50 duplas (10 últimos jogos)
    if len(historico["duplas"]) > 50:
        historico["duplas"] = historico["duplas"][-50:]
    
    with open(HISTORICO_ARQUIVO, 'w') as f:
        json.dump(historico, f)

def encontrar_dupla_balanceada(jogadores, valor_ideal):
    """Encontra uma dupla balanceada considerando histórico"""
    historico = carregar_historico()
    
    # Calcular frequência de cada dupla no histórico
    frequencia = {}
    for dupla in historico["duplas"]:
        dupla_tuple = tuple(dupla)
        if dupla_tuple in frequencia:
            frequencia[dupla_tuple] += 1
        else:
            frequencia[dupla_tuple] = 1
        
        # Considerar também a ordem inversa
        dupla_inversa = (dupla[1], dupla[0])
        if dupla_inversa in frequencia:
            frequencia[dupla_inversa] += 1
        else:
            frequencia[dupla_inversa] = 1
    
    # Avaliar todas as duplas possíveis
    duplas_pontuadas = []
    
    for dupla in combinations(jogadores, 2):
        # Fator de equilíbrio técnico (0 a 10 pontos)
        soma = sum(j['habilidade'] for j in dupla)
        equilibrio = abs(soma - valor_ideal)
        pontos_equilibrio = min(10, equilibrio * 2)
        
        # Fator de histórico (0 a 10 pontos)
        nomes = (dupla[0]['nome'], dupla[1]['nome'])
        nomes_inverso = (dupla[1]['nome'], dupla[0]['nome'])
        vezes_juntos = frequencia.get(nomes, 0) + frequencia.get(nomes_inverso, 0)
        pontos_historico = min(10, vezes_juntos * 2.5)
        
        # Pontuação final (menor é melhor)
        # Priorizamos equilíbrio (60%) e depois variação (40%)
        pontuacao = (pontos_equilibrio * 0.6) + (pontos_historico * 0.4)
        
        duplas_pontuadas.append((dupla, pontuacao, soma))
    
    # Ordenar do melhor para o pior
    duplas_pontuadas.sort(key=lambda x: x[1])
    
    # Escolher aleatoriamente entre as 3 melhores opções
    # (Isso adiciona mais variação enquanto mantém times balanceados)
    top_opcoes = min(3, len(duplas_pontuadas))
    indice = random.randint(0, top_opcoes - 1)
    return duplas_pontuadas[indice][0]

def imprimir_lista_jogadores(times, titulo):
    """Imprime a lista de jogadores formatada"""
    titulo_sem_acento = remover_acentos(titulo)
    print("\n" + "="*80)
    print(titulo_sem_acento.center(80))
    print("="*80)

    print("\nLISTA DE JOGADORES:")
    print("-"*80)
    print(f"{'ZAGUEIROS':<30} {'MEIAS':<30} {'ATACANTES':<30}")
    print("-"*80)

    # Imprimir cada posição separadamente
    max_jogadores = max(len(times[pos]) for pos in POSICOES)
    
    for i in range(max_jogadores):
        linha = []
        
        for pos in POSICOES:
            jogadores_pos = times[pos]
            if i < len(jogadores_pos):
                jogador = jogadores_pos[i]
                nome_limpo = remover_acentos(jogador['nome'])
                pos_sec = '-' if jogador['posicao_secundaria'] == 'nenhum' else jogador['posicao_secundaria']
                linha.append(f"{i+1}- {nome_limpo} ({jogador['habilidade']}) [{pos_sec}]")
            else:
                linha.append("")
        
        print(f"{linha[0]:<30} {linha[1]:<30} {linha[2]}")

    print("-"*80)

def redistribuir_jogadores(times):
    """Redistribui jogadores para balancear os times"""
    # Análise inicial da quantidade de jogadores
    print("\nANÁLISE INICIAL DA DISTRIBUIÇÃO:")
    print("-"*50)
    for pos in POSICOES:
        qtd = len(times[pos])
        print(f"{pos}: {qtd} jogadores")
    print("-"*50)
    
    # Verificar quantos jogadores temos e quantos precisamos em cada posição
    jogadores_alvo = 10  # Queremos exatamente 10 jogadores em cada posição
    excesso_zagueiros = len(times['ZAGUEIROS']) - jogadores_alvo
    excesso_meias = len(times['MEIAS']) - jogadores_alvo
    excesso_atacantes = len(times['ATACANTES']) - jogadores_alvo
    
    print(f"\nExcesso/Falta: ZAGUEIROS: {excesso_zagueiros}, MEIAS: {excesso_meias}, ATACANTES: {excesso_atacantes}")
    
    # Função para mover jogador
    def mover_jogador(jogador, origem, destino, motivo="POSIÇÃO SECUNDÁRIA"):
        times[origem].remove(jogador)
        times[destino].append(jogador)
        times[origem].sort(key=lambda j: j['habilidade'], reverse=True)
        times[destino].sort(key=lambda j: j['habilidade'], reverse=True)
        nome = remover_acentos(jogador['nome'])
        motivo = remover_acentos(motivo)
        print(f"\nMOVENDO POR {motivo}: {nome} ({jogador['habilidade']}) de {origem} para {destino}")
    
    # NOVA LÓGICA: Primeiro identificamos posições com falta de jogadores e priorizamos movimentação
    
    # Identificar posições com falta e excesso
    posicoes_falta = []
    if excesso_zagueiros < 0:
        posicoes_falta.append('ZAGUEIROS')
    if excesso_meias < 0:
        posicoes_falta.append('MEIAS')  
    if excesso_atacantes < 0:
        posicoes_falta.append('ATACANTES')
    
    # Mapeamento de posições secundárias
    mapa_posicao_secundaria = {
        'zagueiro': 'ZAGUEIROS',
        'meia': 'MEIAS',
        'atacante': 'ATACANTES'
    }
    
    # Para cada posição com falta, procurar os melhores jogadores com posição secundária compatível
    for destino in posicoes_falta:
        falta = 0
        if destino == 'ZAGUEIROS':
            falta = abs(excesso_zagueiros)
        elif destino == 'MEIAS':
            falta = abs(excesso_meias)
        else:  # ATACANTES
            falta = abs(excesso_atacantes)
        
        print(f"\n--- ETAPA: PREENCHENDO {destino} (FALTAM {falta}) ---")
        
        # Procurar jogadores de todas as posições que podem ir para a posição com falta
        jogadores_candidatos = []
        
        # Encontrar posição secundária alvo
        posicao_secundaria_alvo = None
        for chave, valor in mapa_posicao_secundaria.items():
            if valor == destino:
                posicao_secundaria_alvo = chave
                break
        
        # Buscar em todas as posições (não apenas nas com excesso)
        for origem in POSICOES:
            # Não processar a mesma posição
            if origem == destino:
                continue
                
            for jogador in times[origem]:
                if jogador['posicao_secundaria'] == posicao_secundaria_alvo:
                    # Calcular um "custo" de movimentação
                    # Se a origem tem excesso, o custo é baixo (0)
                    # Se a origem não tem excesso, o custo é alto (10)
                    custo = 0
                    if (origem == 'ZAGUEIROS' and excesso_zagueiros <= 0) or \
                       (origem == 'MEIAS' and excesso_meias <= 0) or \
                       (origem == 'ATACANTES' and excesso_atacantes <= 0):
                        custo = 10
                    
                    # Calculamos um score baseado na habilidade menos o custo
                    # Jogadores de posições com excesso têm prioridade, mas jogadores
                    # muito bons de outras posições podem ser selecionados mesmo assim
                    score = jogador['habilidade'] - (custo * 0.1)  # Ajuste o peso do custo conforme necessário
                    jogadores_candidatos.append((jogador, origem, score))
        
        # Ordenar candidatos por score (melhores primeiro)
        jogadores_candidatos.sort(key=lambda x: x[2], reverse=True)
        
        print(f"Encontrados {len(jogadores_candidatos)} candidatos com posição secundária {destino}")
        
        # Mover os jogadores necessários
        movidos = 0
        if jogadores_candidatos:  # Verificar se há candidatos antes de tentar movê-los
            for i in range(min(len(jogadores_candidatos), falta)):
                jogador, origem, _ = jogadores_candidatos[i]
                posicao_sec = jogador['posicao_secundaria']
                mover_jogador(jogador, origem, destino, f"{origem[:-1].lower()} QUE JOGA {posicao_sec.upper()}")
                
                # Atualizar contadores
                if origem == 'ZAGUEIROS':
                    excesso_zagueiros -= 1
                elif origem == 'MEIAS':
                    excesso_meias -= 1
                else:  # ATACANTES
                    excesso_atacantes -= 1
                    
                if destino == 'ZAGUEIROS':
                    excesso_zagueiros += 1
                elif destino == 'MEIAS':
                    excesso_meias += 1
                else:  # ATACANTES
                    excesso_atacantes += 1
                
                movidos += 1
            
            if movidos < falta:
                print(f"Atenção: Não foi possível mover todos os jogadores necessários para {destino}. Faltam {falta - movidos}.")
        else:
            print(f"Atenção: Não foram encontrados candidatos com posição secundária {destino}.")
    
    # Recalcular posições com falta após a primeira etapa
    posicoes_falta = []
    if excesso_zagueiros < 0:
        posicoes_falta.append('ZAGUEIROS')
    if excesso_meias < 0:
        posicoes_falta.append('MEIAS')  
    if excesso_atacantes < 0:
        posicoes_falta.append('ATACANTES')
        
    posicoes_excesso = []
    if excesso_zagueiros > 0:
        posicoes_excesso.append('ZAGUEIROS')
    if excesso_meias > 0:
        posicoes_excesso.append('MEIAS')
    if excesso_atacantes > 0:
        posicoes_excesso.append('ATACANTES')
    
    # Se ainda há posições com falta, usar jogadores "coringa" (sem posição secundária)
    if posicoes_falta:
        print("\n--- ETAPA: USANDO CORINGAS PARA FINALIZAR O BALANCEAMENTO ---")
        print(f"Situação atual: ZAGUEIROS: {excesso_zagueiros}, MEIAS: {excesso_meias}, ATACANTES: {excesso_atacantes}")
        
        for destino in posicoes_falta:
            falta = 0
            if destino == 'ZAGUEIROS':
                falta = abs(excesso_zagueiros)
            elif destino == 'MEIAS':
                falta = abs(excesso_meias)
            else:  # ATACANTES
                falta = abs(excesso_atacantes)
            
            # Procurar coringas em posições com excesso
            coringas_candidatos = []
            
            for origem in posicoes_excesso:
                # Não processar a mesma posição
                if origem == destino:
                    continue
                    
                # Encontrar coringas na posição de origem
                for jogador in times[origem]:
                    if jogador['posicao_secundaria'] == 'nenhum':
                        coringas_candidatos.append((jogador, origem))
            
            # Ordenar coringas por habilidade (jogadores com melhores notas primeiro)
            coringas_candidatos.sort(key=lambda x: x[0]['habilidade'], reverse=True)
            
            print(f"Encontrados {len(coringas_candidatos)} coringas nas posições com excesso")
            
            # Mover os coringas necessários
            movidos = 0
            if coringas_candidatos:  # Verificar se a lista não está vazia
                for i in range(min(len(coringas_candidatos), falta)):
                    jogador, origem = coringas_candidatos[i]
                    mover_jogador(jogador, origem, destino, "CORINGA")
                    
                    # Atualizar contadores
                    if origem == 'ZAGUEIROS':
                        excesso_zagueiros -= 1
                    elif origem == 'MEIAS':
                        excesso_meias -= 1
                    else:  # ATACANTES
                        excesso_atacantes -= 1
                        
                    if destino == 'ZAGUEIROS':
                        excesso_zagueiros += 1
                    elif destino == 'MEIAS':
                        excesso_meias += 1
                    else:  # ATACANTES
                        excesso_atacantes += 1
                        
                    # Remover o jogador da lista de candidatos
                    coringas_candidatos = [(j, o) for j, o in coringas_candidatos if j != jogador]
                    movidos += 1
                
                if movidos < falta:
                    print(f"Atenção: Não foi possível mover todos os coringas necessários para {destino}. Faltam {falta - movidos}.")
            else:
                print(f"Atenção: Não foram encontrados coringas nas posições com excesso para mover para {destino}.")
                
                # Tentar usar jogadores com pior habilidade de qualquer posição com excesso
                print(f"Tentando usar jogadores de menor habilidade de qualquer posição com excesso...")
                jogadores_alternativos = []
                
                for origem in posicoes_excesso:
                    if origem != destino and len(times[origem]) > jogadores_alvo:
                        # Ordenar jogadores por habilidade (menor primeiro)
                        jogadores_origem = sorted(times[origem], key=lambda j: j['habilidade'])
                        # Adicionar jogadores suficientes
                        excesso = len(times[origem]) - jogadores_alvo
                        jogadores_alternativos.extend([(j, origem) for j in jogadores_origem[:excesso]])
                
                # Ordenar por habilidade (menor primeiro)
                jogadores_alternativos.sort(key=lambda x: x[0]['habilidade'])
                
                # Mover jogadores alternativos
                for i in range(min(len(jogadores_alternativos), falta - movidos)):
                    jogador, origem = jogadores_alternativos[i]
                    mover_jogador(jogador, origem, destino, "ALTERNATIVO (MENOR HABILIDADE)")
                    
                    # Atualizar contadores
                    if origem == 'ZAGUEIROS':
                        excesso_zagueiros -= 1
                    elif origem == 'MEIAS':
                        excesso_meias -= 1
                    else:  # ATACANTES
                        excesso_atacantes -= 1
                        
                    if destino == 'ZAGUEIROS':
                        excesso_zagueiros += 1
                    elif destino == 'MEIAS':
                        excesso_meias += 1
                    else:  # ATACANTES
                        excesso_atacantes += 1
                    
                    movidos += 1
    
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
print("\n" + "="*80)
print("DISTRIBUIÇÃO INICIAL DOS JOGADORES".center(80))
print("="*80)
print("\nQuantidade inicial de jogadores por posição:")
for pos in POSICOES:
    print(f"- {pos}: {len(times[pos])} jogadores")

imprimir_lista_jogadores(times, "JOGADORES POR POSIÇÃO (INICIAL)")

# Redistribuir jogadores
times = redistribuir_jogadores(times)

# Imprimir lista após redistribuição
print("\n" + "="*80)
print("RESULTADO FINAL APÓS REDISTRIBUIÇÃO".center(80))
print("="*80)
print("\nQuantidade final de jogadores por posição:")
for pos in POSICOES:
    print(f"- {pos}: {len(times[pos])} jogadores")

imprimir_lista_jogadores(times, "JOGADORES POR POSIÇÃO (APÓS REDISTRIBUIÇÃO)")

# Calcular somas
soma_total = sum(sum(j['habilidade'] for j in times[pos]) for pos in POSICOES)
meta_notas = soma_total / 3
somas = {pos: sum(j['habilidade'] for j in times[pos]) for pos in POSICOES}

print("\n" + "="*100)
print("SOMA TOTAL DAS NOTAS: {:.1f} pontos".format(soma_total))
print("META POR POSIÇÃO: {:.2f} pontos (Total {:.1f} / 3 posições)".format(meta_notas, soma_total))
print("META POR TIME (5 TIMES): {:.2f} pontos (Total {:.1f} / 5 times)".format(soma_total/5, soma_total))
print("="*100)

print("\nSOMA DAS NOTAS POR POSIÇÃO:")
print("-"*100)
for pos in POSICOES:
    diferenca = somas[pos] - meta_notas
    sinal = "+" if diferenca > 0 else ""
    print(f"{pos:<15} -> {somas[pos]:>5.1f} pontos (Meta: {meta_notas:.2f}) [{sinal}{diferenca:.2f}]")
    print(f"               -> {somas[pos]/5:>5.1f} pontos por time (2 jogadores)")
print("-"*100)

print("\n")  # Adicione uma linha em branco para separar as seções


# Inicializar estrutura dos times
times_montados = {i: {'ZAGUEIROS': [], 'MEIAS': [], 'ATACANTES': [], 'total': 0} for i in range(1, NUM_TIMES + 1)}

# Lista para armazenar as novas duplas formadas
duplas_formadas = []

# Distribuir jogadores para cada posição
for pos in POSICOES:
    jogadores_disponiveis = deepcopy(times[pos])
    valor_ideal = somas[pos] / NUM_TIMES
    
    # Distribuir para os primeiros N-1 times
    for time_num in range(1, NUM_TIMES):
        if len(jogadores_disponiveis) >= 2:
            # Usar a nova função que considera o histórico
            dupla = encontrar_dupla_balanceada(jogadores_disponiveis, valor_ideal)
            if dupla:
                times_montados[time_num][pos].extend(dupla)
                times_montados[time_num]['total'] += sum(j['habilidade'] for j in dupla)
                for jogador in dupla:
                    jogadores_disponiveis.remove(jogador)
                
                # Registrar a dupla formada
                duplas_formadas.append(dupla)
    
    # Último time recebe os jogadores restantes
    if len(jogadores_disponiveis) == 2:
        times_montados[NUM_TIMES][pos].extend(jogadores_disponiveis)
        times_montados[NUM_TIMES]['total'] += sum(j['habilidade'] for j in jogadores_disponiveis)
        
        # Registrar também esta dupla
        duplas_formadas.append(tuple(jogadores_disponiveis))

# Salvar histórico atualizado
salvar_historico(duplas_formadas)

# Imprimir informação sobre o histórico
historico = carregar_historico()
print("\nINFORMACOES SOBRE HISTORICO DE DUPLAS:")
print(f"Total de duplas no historico: {len(historico['duplas'])}")
print(f"Novas duplas formadas: {len(duplas_formadas)}")
print("-"*100)

# Imprimir times no novo formato
def imprimir_times_novo_formato(times_montados):
    """Imprime os times no novo formato"""
    print("\nTimes Sorteados\n")
    
    # Verificar se algum time tem mais de 2 jogadores por posição
    for time_num in range(1, NUM_TIMES + 1):
        for pos in POSICOES:
            # Se tiver mais de 2 jogadores, manter apenas os 2 primeiros (melhores)
            if len(times_montados[time_num][pos]) > 2:
                print(f"AVISO: Time {time_num} tem {len(times_montados[time_num][pos])} jogadores na posição {pos}. Mantendo apenas os 2 melhores.")
                jogadores_excluidos = times_montados[time_num][pos][2:]
                for jogador in jogadores_excluidos:
                    times_montados[time_num]['total'] -= jogador['habilidade']
                times_montados[time_num][pos] = times_montados[time_num][pos][:2]
    
    for time_num in range(1, NUM_TIMES + 1):
        time = times_montados[time_num]
        
        # Calcular total de estrelas (apenas dos jogadores que serão exibidos)
        total_estrelas = 0
        for pos in POSICOES:
            total_estrelas += sum(j['habilidade'] for j in time[pos][:2])  # Considerar apenas os 2 primeiros
        
        # Imprimir cabeçalho do time
        print(f"--------------- Time {time_num} ---------------")
        print(f"Time {time_num} | {total_estrelas:.1f} Estrelas\n")
        
        # Imprimir jogadores (máximo 2 por posição)
        for pos in POSICOES:
            for jogador in time[pos][:2]:  # Limitar a 2 jogadores por posição
                pos_atual = pos[:3]  # Pega as 3 primeiras letras da posição atual
                nome_limpo = remover_acentos(jogador['nome'])
                print(f"{nome_limpo} | {jogador['habilidade']} Estrelas | {pos_atual}")
        
        print()

def redistribuir_jogadores_fracos(times_montados, nota_corte=3.0):
    """
    Redistribui jogadores fracos (com nota abaixo do corte) para evitar que um time
    fique com muitos jogadores de baixa habilidade ou com vários na mesma posição.
    """
    print("\n" + "="*80)
    print("REDISTRIBUIÇÃO DE JOGADORES FRACOS".center(80))
    print("="*80)
    
    # Primeiro, vamos identificar todos os jogadores "fracos"
    jogadores_fracos = []
    for time_num in range(1, NUM_TIMES + 1):
        for pos in POSICOES:
            for jogador in times_montados[time_num][pos]:
                if jogador['habilidade'] < nota_corte:
                    jogadores_fracos.append((jogador, time_num, pos))
    
    # Ordenar os jogadores fracos por habilidade (do mais baixo para o mais alto)
    jogadores_fracos.sort(key=lambda x: x[0]['habilidade'])
    
    print(f"\nIdentificados {len(jogadores_fracos)} jogadores com nota abaixo de {nota_corte}:")
    for jogador, time_num, pos in jogadores_fracos:
        nome_limpo = remover_acentos(jogador['nome'])
        print(f"- {nome_limpo} ({jogador['habilidade']}) | Time {time_num} | {pos}")
    
    # 1. Verificar a distribuição total de jogadores fracos por time
    times_com_fracos = {}
    for time_num in range(1, NUM_TIMES + 1):
        times_com_fracos[time_num] = sum(1 for j, t, _ in jogadores_fracos if t == time_num)
    
    print("\nDistribuição inicial de jogadores fracos por time:")
    for time_num, count in times_com_fracos.items():
        print(f"Time {time_num}: {count} jogadores fracos")
    
    # 2. Verificar a distribuição por posição em cada time
    problemas_por_posicao = False
    for time_num in range(1, NUM_TIMES + 1):
        fracos_por_posicao = {pos: 0 for pos in POSICOES}
        for _, t, pos in jogadores_fracos:
            if t == time_num:
                fracos_por_posicao[pos] += 1
        
        print(f"\nTime {time_num} - Distribuição por posição:")
        for pos, qtd in fracos_por_posicao.items():
            print(f"- {pos}: {qtd} jogadores fracos")
            # Se um time tem mais de um jogador fraco na mesma posição, isso é um problema
            if qtd > 1:
                problemas_por_posicao = True
    
    # Verificar se precisamos redistribuir
    valores_unicos = set(times_com_fracos.values())
    balanco_total_ok = len(valores_unicos) == 1 or (len(valores_unicos) == 2 and max(valores_unicos) - min(valores_unicos) <= 1)
    
    # Também verificar se há times com mais de um jogador fraco no total
    times_com_multiplos_fracos = [time_num for time_num, count in times_com_fracos.items() if count > 1]
    
    if balanco_total_ok and not problemas_por_posicao and not times_com_multiplos_fracos:
        print("\nA distribuição já está balanceada. Não é necessário redistribuir.")
        return times_montados
    
    # Se chegamos aqui, precisamos redistribuir
    print("\nIniciando redistribuição para balancear jogadores fracos...")
    if problemas_por_posicao:
        print("- Motivo: Existem times com mais de um jogador fraco na mesma posição")
    if not balanco_total_ok:
        print("- Motivo: A distribuição total de jogadores fracos não está equilibrada entre os times")
    if times_com_multiplos_fracos:
        print(f"- Motivo: Existem times com mais de um jogador fraco: {times_com_multiplos_fracos}")
    
    # Remover todos os jogadores fracos dos times
    jogadores_removidos = []
    for jogador, time_num, pos in jogadores_fracos:
        times_montados[time_num][pos].remove(jogador)
        times_montados[time_num]['total'] -= jogador['habilidade']
        jogadores_removidos.append((jogador, pos))
    
    # Agrupar jogadores por posição
    jogadores_por_posicao = {pos: [] for pos in POSICOES}
    for jogador, pos in jogadores_removidos:
        jogadores_por_posicao[pos].append(jogador)
    
    # Redistribuir jogadores fracos, garantindo que cada time tenha no máximo um jogador fraco por posição
    # e que a distribuição total de jogadores fracos seja equilibrada entre os times
    
    # Primeiro, criar uma lista de times para distribuição
    # Vamos ordenar os times para receber jogadores do mais forte para o mais fraco
    # para equilibrar um pouco a força dos times
    times_ordenados = [(time_num, times_montados[time_num]['total']) for time_num in range(1, NUM_TIMES + 1)]
    times_ordenados.sort(key=lambda x: x[1], reverse=True)  # Ordenar do mais forte para o mais fraco
    
    # Contagem de jogadores fracos adicionados a cada time após redistribuição
    fracos_adicionados = {time_num: 0 for time_num in range(1, NUM_TIMES + 1)}
    # Posições já ocupadas por jogadores fracos em cada time
    posicoes_ocupadas = {time_num: set() for time_num in range(1, NUM_TIMES + 1)}
    
    # Distribuir jogadores por posição
    for pos in POSICOES:
        jogadores_pos = jogadores_por_posicao[pos]
        # Ordenar jogadores por habilidade (menor primeiro)
        jogadores_pos.sort(key=lambda j: j['habilidade'])
        
        # Distribuir jogadores desta posição
        for jogador in jogadores_pos:
            # Encontrar melhor time para este jogador
            melhor_time = None
            for time_num, _ in times_ordenados:
                # Se este time já tem um jogador fraco nesta posição, pular
                if pos in posicoes_ocupadas[time_num]:
                    continue
                
                # Se encontramos um time sem jogador fraco nesta posição, usar este
                melhor_time = time_num
                # Priorizar times com menos jogadores fracos
                if fracos_adicionados[time_num] == 0:
                    break
            
            # Se não encontramos um time adequado, usar o time com menos jogadores fracos
            if melhor_time is None:
                melhor_time = min(fracos_adicionados.items(), key=lambda x: x[1])[0]
            
            # Adicionar jogador ao time escolhido
            times_montados[melhor_time][pos].append(jogador)
            times_montados[melhor_time]['total'] += jogador['habilidade']
            
            # Atualizar contadores
            fracos_adicionados[melhor_time] += 1
            posicoes_ocupadas[melhor_time].add(pos)
            
            nome_limpo = remover_acentos(jogador['nome'])
            print(f"Movendo {nome_limpo} ({jogador['habilidade']}) para Time {melhor_time} | {pos}")
    
    # Ordenar jogadores por habilidade em cada posição
    for time_num in range(1, NUM_TIMES + 1):
        for pos in POSICOES:
            times_montados[time_num][pos].sort(key=lambda j: j['habilidade'], reverse=True)
    
    # Verificar nova distribuição
    nova_dist = {time_num: 0 for time_num in range(1, NUM_TIMES + 1)}
    for time_num in range(1, NUM_TIMES + 1):
        for pos in POSICOES:
            jogadores_fracos_pos = [j for j in times_montados[time_num][pos] if j['habilidade'] < nota_corte]
            nova_dist[time_num] += len(jogadores_fracos_pos)
            
            if len(jogadores_fracos_pos) > 0:
                print(f"Time {time_num} | {pos}: {len(jogadores_fracos_pos)} jogadores fracos")
    
    print("\nNova distribuição de jogadores fracos por time:")
    for time_num, count in nova_dist.items():
        print(f"Time {time_num}: {count} jogadores fracos")
    
    return times_montados

# Embaralhar a ordem dos times
ordem_times = list(range(1, NUM_TIMES + 1))
random.shuffle(ordem_times)

# Criar um dicionário para mapear a nova ordem
mapeamento = {i+1: ordem_times[i] for i in range(NUM_TIMES)}

# Redistribuir jogadores fracos antes de imprimir
times_montados = redistribuir_jogadores_fracos(times_montados, nota_corte=3.0)

# Chamar a função para imprimir os times
imprimir_times_novo_formato(times_montados)