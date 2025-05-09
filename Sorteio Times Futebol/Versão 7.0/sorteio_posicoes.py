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
    
    # ETAPA 1: Balancear zagueiros e meias
    if excesso_zagueiros > 0 and excesso_meias < 0:
        print("\n--- ETAPA 1: MOVENDO ZAGUEIROS QUE JOGAM DE MEIA ---")
        
        # Quantos zagueiros precisamos mover para meias
        mover_zag_para_meias = min(excesso_zagueiros, abs(excesso_meias))
        
        # Encontrar zagueiros que jogam de meia
        zagueiros_meias = []
        for jogador in times['ZAGUEIROS']:
            if jogador['posicao_secundaria'] == 'meia':
                zagueiros_meias.append(jogador)
        
        # Ordenar por habilidade (maiores primeiro)
        zagueiros_meias.sort(key=lambda j: j['habilidade'], reverse=True)
        
        print(f"Encontrados {len(zagueiros_meias)} zagueiros que jogam de meia")
        
        # Mover os necessários
        for i in range(min(len(zagueiros_meias), mover_zag_para_meias)):
            mover_jogador(zagueiros_meias[i], 'ZAGUEIROS', 'MEIAS', "ZAGUEIRO QUE JOGA MEIA")
            excesso_zagueiros -= 1
            excesso_meias += 1
    
    # ETAPA 2: Balancear atacantes e meias
    if excesso_atacantes > 0 and excesso_meias < 0:
        print("\n--- ETAPA 2: MOVENDO ATACANTES QUE JOGAM DE MEIA ---")
        
        # Quantos atacantes precisamos mover para meias
        mover_atac_para_meias = min(excesso_atacantes, abs(excesso_meias))
        
        # Encontrar atacantes que jogam de meia
        atacantes_meias = []
        for jogador in times['ATACANTES']:
            if jogador['posicao_secundaria'] == 'meia':
                atacantes_meias.append(jogador)
        
        # Ordenar por habilidade (maiores primeiro)
        atacantes_meias.sort(key=lambda j: j['habilidade'], reverse=True)
        
        print(f"Encontrados {len(atacantes_meias)} atacantes que jogam de meia")
        
        # Mover os necessários
        for i in range(min(len(atacantes_meias), mover_atac_para_meias)):
            mover_jogador(atacantes_meias[i], 'ATACANTES', 'MEIAS', "ATACANTE QUE JOGA MEIA")
            excesso_atacantes -= 1
            excesso_meias += 1
    
    # ETAPA 3: Balancear meias e zagueiros
    if excesso_meias > 0 and excesso_zagueiros < 0:
        print("\n--- ETAPA 3: MOVENDO MEIAS QUE JOGAM DE ZAGUEIRO ---")
        
        # Quantos meias precisamos mover para zagueiros
        mover_meias_para_zag = min(excesso_meias, abs(excesso_zagueiros))
        
        # Encontrar meias que jogam de zagueiro
        meias_zagueiros = []
        for jogador in times['MEIAS']:
            if jogador['posicao_secundaria'] == 'zagueiro':
                meias_zagueiros.append(jogador)
        
        # Ordenar por habilidade (maiores primeiro)
        meias_zagueiros.sort(key=lambda j: j['habilidade'], reverse=True)
        
        print(f"Encontrados {len(meias_zagueiros)} meias que jogam de zagueiro")
        
        # Mover os necessários
        for i in range(min(len(meias_zagueiros), mover_meias_para_zag)):
            mover_jogador(meias_zagueiros[i], 'MEIAS', 'ZAGUEIROS', "MEIA QUE JOGA ZAGUEIRO")
            excesso_meias -= 1
            excesso_zagueiros += 1
    
    # ETAPA 4: Balancear meias e atacantes
    if excesso_meias > 0 and excesso_atacantes < 0:
        print("\n--- ETAPA 4: MOVENDO MEIAS QUE JOGAM DE ATACANTE ---")
        
        # Quantos meias precisamos mover para atacantes
        mover_meias_para_atac = min(excesso_meias, abs(excesso_atacantes))
        
        # Encontrar meias que jogam de atacante
        meias_atacantes = []
        for jogador in times['MEIAS']:
            if jogador['posicao_secundaria'] == 'atacante':
                meias_atacantes.append(jogador)
        
        # Ordenar por habilidade (maiores primeiro)
        meias_atacantes.sort(key=lambda j: j['habilidade'], reverse=True)
        
        print(f"Encontrados {len(meias_atacantes)} meias que jogam de atacante")
        
        # Mover os necessários
        for i in range(min(len(meias_atacantes), mover_meias_para_atac)):
            mover_jogador(meias_atacantes[i], 'MEIAS', 'ATACANTES', "MEIA QUE JOGA ATACANTE")
            excesso_meias -= 1
            excesso_atacantes += 1
    
    # ETAPA 5: Balancear zagueiros e atacantes (se necessário)
    if excesso_zagueiros > 0 and excesso_atacantes < 0:
        print("\n--- ETAPA 5: MOVENDO ZAGUEIROS QUE JOGAM DE ATACANTE ---")
        
        # Quantos zagueiros precisamos mover para atacantes
        mover_zag_para_atac = min(excesso_zagueiros, abs(excesso_atacantes))
        
        # Encontrar zagueiros que jogam de atacante
        zagueiros_atacantes = []
        for jogador in times['ZAGUEIROS']:
            if jogador['posicao_secundaria'] == 'atacante':
                zagueiros_atacantes.append(jogador)
        
        # Ordenar por habilidade (maiores primeiro)
        zagueiros_atacantes.sort(key=lambda j: j['habilidade'], reverse=True)
        
        print(f"Encontrados {len(zagueiros_atacantes)} zagueiros que jogam de atacante")
        
        # Mover os necessários
        for i in range(min(len(zagueiros_atacantes), mover_zag_para_atac)):
            mover_jogador(zagueiros_atacantes[i], 'ZAGUEIROS', 'ATACANTES', "ZAGUEIRO QUE JOGA ATACANTE")
            excesso_zagueiros -= 1
            excesso_atacantes += 1
    
    # ETAPA 6: Balancear atacantes e zagueiros (se necessário)
    if excesso_atacantes > 0 and excesso_zagueiros < 0:
        print("\n--- ETAPA 6: MOVENDO ATACANTES QUE JOGAM DE ZAGUEIRO ---")
        
        # Quantos atacantes precisamos mover para zagueiros
        mover_atac_para_zag = min(excesso_atacantes, abs(excesso_zagueiros))
        
        # Encontrar atacantes que jogam de zagueiro
        atacantes_zagueiros = []
        for jogador in times['ATACANTES']:
            if jogador['posicao_secundaria'] == 'zagueiro':
                atacantes_zagueiros.append(jogador)
        
        # Ordenar por habilidade (maiores primeiro)
        atacantes_zagueiros.sort(key=lambda j: j['habilidade'], reverse=True)
        
        print(f"Encontrados {len(atacantes_zagueiros)} atacantes que jogam de zagueiro")
        
        # Mover os necessários
        for i in range(min(len(atacantes_zagueiros), mover_atac_para_zag)):
            mover_jogador(atacantes_zagueiros[i], 'ATACANTES', 'ZAGUEIROS', "ATACANTE QUE JOGA ZAGUEIRO")
            excesso_atacantes -= 1
            excesso_zagueiros += 1
    
    # ETAPA 7: Usar coringas (jogadores sem posição secundária) para finalizar o balanceamento
    print("\n--- ETAPA 7: USANDO CORINGAS PARA FINALIZAR O BALANCEAMENTO ---")
    
    # Recalcular os excessos após as etapas anteriores
    excesso_zagueiros = len(times['ZAGUEIROS']) - jogadores_alvo
    excesso_meias = len(times['MEIAS']) - jogadores_alvo
    excesso_atacantes = len(times['ATACANTES']) - jogadores_alvo
    
    print(f"Situação atual: ZAGUEIROS: {excesso_zagueiros}, MEIAS: {excesso_meias}, ATACANTES: {excesso_atacantes}")
    
    # Mover coringas zagueiros, se necessário
    if excesso_zagueiros > 0:
        # Encontrar zagueiros que são coringas
        zagueiros_coringas = []
        for jogador in times['ZAGUEIROS']:
            if jogador['posicao_secundaria'] == 'nenhum':
                zagueiros_coringas.append(jogador)
        
        # Ordenar por habilidade (menores primeiro para mover os mais fracos)
        zagueiros_coringas.sort(key=lambda j: j['habilidade'])
        
        print(f"Encontrados {len(zagueiros_coringas)} zagueiros coringas")
        
        # Mover para meias, se necessário
        if excesso_meias < 0:
            mover_zag_para_meias = min(excesso_zagueiros, abs(excesso_meias), len(zagueiros_coringas))
            for i in range(mover_zag_para_meias):
                mover_jogador(zagueiros_coringas[i], 'ZAGUEIROS', 'MEIAS', "CORINGA")
                excesso_zagueiros -= 1
                excesso_meias += 1
                zagueiros_coringas = [j for j in zagueiros_coringas if j not in times['MEIAS']]
        
        # Se ainda temos excesso e falta em atacantes
        if excesso_zagueiros > 0 and excesso_atacantes < 0 and zagueiros_coringas:
            mover_zag_para_atac = min(excesso_zagueiros, abs(excesso_atacantes), len(zagueiros_coringas))
            for i in range(mover_zag_para_atac):
                mover_jogador(zagueiros_coringas[i], 'ZAGUEIROS', 'ATACANTES', "CORINGA")
                excesso_zagueiros -= 1
                excesso_atacantes += 1
    
    # Mover coringas meias, se necessário
    if excesso_meias > 0:
        # Encontrar meias que são coringas
        meias_coringas = []
        for jogador in times['MEIAS']:
            if jogador['posicao_secundaria'] == 'nenhum':
                meias_coringas.append(jogador)
        
        # Ordenar por habilidade (menores primeiro para mover os mais fracos)
        meias_coringas.sort(key=lambda j: j['habilidade'])
        
        print(f"Encontrados {len(meias_coringas)} meias coringas")
        
        # Mover para zagueiros, se necessário
        if excesso_zagueiros < 0:
            mover_meias_para_zag = min(excesso_meias, abs(excesso_zagueiros), len(meias_coringas))
            for i in range(mover_meias_para_zag):
                mover_jogador(meias_coringas[i], 'MEIAS', 'ZAGUEIROS', "CORINGA")
                excesso_meias -= 1
                excesso_zagueiros += 1
                meias_coringas = [j for j in meias_coringas if j not in times['ZAGUEIROS']]
        
        # Se ainda temos excesso e falta em atacantes
        if excesso_meias > 0 and excesso_atacantes < 0 and meias_coringas:
            mover_meias_para_atac = min(excesso_meias, abs(excesso_atacantes), len(meias_coringas))
            for i in range(mover_meias_para_atac):
                mover_jogador(meias_coringas[i], 'MEIAS', 'ATACANTES', "CORINGA")
                excesso_meias -= 1
                excesso_atacantes += 1
    
    # Mover coringas atacantes, se necessário
    if excesso_atacantes > 0:
        # Encontrar atacantes que são coringas
        atacantes_coringas = []
        for jogador in times['ATACANTES']:
            if jogador['posicao_secundaria'] == 'nenhum':
                atacantes_coringas.append(jogador)
        
        # Ordenar por habilidade (menores primeiro para mover os mais fracos)
        atacantes_coringas.sort(key=lambda j: j['habilidade'])
        
        print(f"Encontrados {len(atacantes_coringas)} atacantes coringas")
        
        # Mover para zagueiros, se necessário
        if excesso_zagueiros < 0:
            mover_atac_para_zag = min(excesso_atacantes, abs(excesso_zagueiros), len(atacantes_coringas))
            for i in range(mover_atac_para_zag):
                mover_jogador(atacantes_coringas[i], 'ATACANTES', 'ZAGUEIROS', "CORINGA")
                excesso_atacantes -= 1
                excesso_zagueiros += 1
                atacantes_coringas = [j for j in atacantes_coringas if j not in times['ZAGUEIROS']]
        
        # Se ainda temos excesso e falta em meias
        if excesso_atacantes > 0 and excesso_meias < 0 and atacantes_coringas:
            mover_atac_para_meias = min(excesso_atacantes, abs(excesso_meias), len(atacantes_coringas))
            for i in range(mover_atac_para_meias):
                mover_jogador(atacantes_coringas[i], 'ATACANTES', 'MEIAS', "CORINGA")
                excesso_atacantes -= 1
                excesso_meias += 1
    
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

# Embaralhar a ordem dos times
ordem_times = list(range(1, NUM_TIMES + 1))
random.shuffle(ordem_times)

# Criar um dicionário para mapear a nova ordem
mapeamento = {i+1: ordem_times[i] for i in range(NUM_TIMES)}

# Chamar a função para imprimir os times
imprimir_times_novo_formato(times_montados)