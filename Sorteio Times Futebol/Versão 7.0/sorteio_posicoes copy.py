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