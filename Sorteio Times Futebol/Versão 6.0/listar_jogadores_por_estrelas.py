"""
Script para listar jogadores por posição primária e jogadores versáteis
"""

from modulos.jogadores import carregar_jogadores
import random
import os
import datetime
import sys

def balancear_posicoes(posicoes):
    """
    Balanceia as posições para que cada uma tenha idealmente 10 jogadores.
    A estratégia é:
    1. Identificar posições com excesso e falta de jogadores
    2. Mover jogadores das posições com excesso para posições com falta
    3. Escolher jogadores que têm a posição secundária compatível
    4. Selecionar aleatoriamente os jogadores dentro das possibilidades
    """
    # Número ideal de jogadores por posição
    NUM_IDEAL = 10
    
    # Função para mover jogador entre posições
    def mover_jogador(jogador, origem, destino):
        # Remove da origem
        if jogador in posicoes[origem]['primaria']:
            posicoes[origem]['primaria'].remove(jogador)
        else:
            posicoes[origem]['versateis'].remove(jogador)
        
        # Adiciona ao destino
        posicoes[destino]['versateis'].append(jogador)
        print(f"\nMovendo {jogador['nome']} de {origem[:-1].capitalize()} para {destino[:-1].capitalize()}")
    
    # Função para contar total de jogadores em uma posição
    def contar_jogadores(pos):
        return len(posicoes[pos]['primaria']) + len(posicoes[pos]['versateis'])
    
    # Função para encontrar candidatos a mudança
    def encontrar_candidatos(origem, destino):
        candidatos = []
        # Remove 's' do final (ex: 'zagueiros' -> 'zagueiro')
        destino_singular = destino[:-1]
        
        # Procura jogadores que têm a posição secundária compatível
        for jogador in posicoes[origem]['primaria'] + posicoes[origem]['versateis']:
            if jogador['posicao_secundaria'] == destino_singular:
                candidatos.append(jogador)
        
        # Embaralha a lista para adicionar aleatoriedade
        random.shuffle(candidatos)
        
        return candidatos
    
    # Situação inicial
    total_zagueiros = contar_jogadores('zagueiros')
    total_meias = contar_jogadores('meias')
    total_atacantes = contar_jogadores('atacantes')
    
    print("\nTotal inicial de jogadores por posição:")
    print(f"Zagueiros: {total_zagueiros}")
    print(f"Meias: {total_meias}")
    print(f"Atacantes: {total_atacantes}")
    
    # Casos especiais mais comuns
    
    # Caso 1: Falta zagueiro (9) e sobra atacante (11)
    if total_zagueiros == 9 and total_atacantes == 11:
        # Procura atacantes que podem jogar como zagueiro
        candidatos = encontrar_candidatos('atacantes', 'zagueiros')
        if candidatos:
            # Escolhe um jogador aleatoriamente
            jogador = random.choice(candidatos)
            mover_jogador(jogador, 'atacantes', 'zagueiros')
        else:
            # Tentar encontrar meia que joga de zagueiro
            candidatos = encontrar_candidatos('meias', 'zagueiros')
            if candidatos and total_meias > 9:
                # Escolhe um jogador aleatoriamente
                jogador = random.choice(candidatos)
                mover_jogador(jogador, 'meias', 'zagueiros')
    
    # Caso 2: Falta meia (9) e sobra atacante (11)  
    elif total_meias == 9 and total_atacantes == 11:
        # Procura atacantes que podem jogar como meia
        candidatos = encontrar_candidatos('atacantes', 'meias')
        if candidatos:
            # Escolhe um jogador aleatoriamente
            jogador = random.choice(candidatos)
            mover_jogador(jogador, 'atacantes', 'meias')
    
    # Caso 3: Falta zagueiro (9) e sobra meia (11)
    elif total_zagueiros == 9 and total_meias == 11:
        # Procura meias que podem jogar como zagueiro
        candidatos = encontrar_candidatos('meias', 'zagueiros')
        if candidatos:
            # Escolhe um jogador aleatoriamente
            jogador = random.choice(candidatos)
            mover_jogador(jogador, 'meias', 'zagueiros')
    
    # Verificar novamente os totais
    total_zagueiros = contar_jogadores('zagueiros')
    total_meias = contar_jogadores('meias')
    total_atacantes = contar_jogadores('atacantes')
    
    print("\nTotal após ajustes específicos:")
    print(f"Zagueiros: {total_zagueiros}")
    print(f"Meias: {total_meias}")
    print(f"Atacantes: {total_atacantes}")
    
    # Se ainda precisar de balanceamento, tenta um balanceamento genérico
    if total_zagueiros != 10 or total_meias != 10 or total_atacantes != 10:
        print("\nTentando balanceamento genérico...")
        
        # Tenta balancear jogadores
        for _ in range(3):  # no máximo 3 tentativas
            # Verificar quais posições têm excesso (mais de 10) e quais têm falta (menos de 10)
            posicoes_com_excesso = []
            posicoes_com_falta = []
            
            if total_zagueiros > 10:
                posicoes_com_excesso.append('zagueiros')
            elif total_zagueiros < 10:
                posicoes_com_falta.append('zagueiros')
                
            if total_meias > 10:
                posicoes_com_excesso.append('meias')
            elif total_meias < 10:
                posicoes_com_falta.append('meias')
                
            if total_atacantes > 10:
                posicoes_com_excesso.append('atacantes')
            elif total_atacantes < 10:
                posicoes_com_falta.append('atacantes')
            
            # Se não há posições com excesso ou com falta, termina
            if not posicoes_com_excesso or not posicoes_com_falta:
                break
            
            # Randomiza a ordem das posições de destino para adicionar variabilidade
            random.shuffle(posicoes_com_falta)
            
            # Tenta mover jogadores de posições com excesso para posições com falta
            mudanca_feita = False
            for destino in posicoes_com_falta:
                # Randomiza a ordem das posições de origem para adicionar variabilidade
                posicoes_com_excesso_random = posicoes_com_excesso.copy()
                random.shuffle(posicoes_com_excesso_random)
                
                for origem in posicoes_com_excesso_random:
                    candidatos = encontrar_candidatos(origem, destino)
                    if candidatos:
                        # Escolhe um jogador aleatoriamente entre os candidatos
                        jogador = random.choice(candidatos)
                        mover_jogador(jogador, origem, destino)
                        
                        # Atualiza os totais
                        total_zagueiros = contar_jogadores('zagueiros')
                        total_meias = contar_jogadores('meias')
                        total_atacantes = contar_jogadores('atacantes')
                        
                        mudanca_feita = True
                        break
                
                if mudanca_feita:
                    break
            
            # Se não conseguiu fazer nenhuma mudança, termina o loop
            if not mudanca_feita:
                break
    
    # Resultado final
    total_zagueiros = contar_jogadores('zagueiros')
    total_meias = contar_jogadores('meias')
    total_atacantes = contar_jogadores('atacantes')
    
    print("\nBalanceamento concluído. Total final de jogadores por posição:")
    print(f"Zagueiros: {total_zagueiros}")
    print(f"Meias: {total_meias}")
    print(f"Atacantes: {total_atacantes}")
    
    # Se não conseguiu balancear perfeitamente, mostra uma mensagem
    if total_zagueiros != 10 or total_meias != 10 or total_atacantes != 10:
        print("\nNão foi possível balancear perfeitamente as posições com os jogadores disponíveis.")
        print("Isso pode ocorrer quando não há jogadores versatéis suficientes para fazer as trocas necessárias.")

def agrupar_por_estrelas(jogadores):
    """
    Agrupa jogadores por número de estrelas.
    Retorna um dicionário onde a chave é o número de estrelas e o valor é a lista de jogadores.
    """
    grupos = {}
    for jogador in jogadores:
        estrelas = jogador['habilidade']
        if estrelas not in grupos:
            grupos[estrelas] = []
        grupos[estrelas].append(jogador)
    return dict(sorted(grupos.items(), reverse=True))  # Ordena por estrelas (decrescente)

def distribuir_jogadores_por_estrelas(jogadores_lista):
    """
    Distribui os jogadores em 5 pares, garantindo que os 5 piores jogadores fiquem em times diferentes,
    seguidos pelos 5 melhores jogadores também em times diferentes.
    Evita que um time tenha mais de um jogador com nota menor que 3, a menos que seja inevitável.
    Retorna uma lista de 5 pares de jogadores (melhor, pior).
    """
    # Ordena todos os jogadores por habilidade (crescente)
    jogadores_ordenados = sorted(jogadores_lista, key=lambda x: (x['habilidade'], x['nome']))
    
    # Separa jogadores com habilidade < 3
    jogadores_fracos_3 = [j for j in jogadores_ordenados if j['habilidade'] < 3]
    
    # Pega os jogadores com menor pontuação (1, 2.5 e 3 estrelas)
    jogadores_fracos = [j for j in jogadores_ordenados if j['habilidade'] <= 3]
    # Se não tiver 5 jogadores fracos, completa com os próximos piores
    if len(jogadores_fracos) < 5:
        jogadores_restantes = [j for j in jogadores_ordenados if j not in jogadores_fracos]
        jogadores_fracos.extend(jogadores_restantes[:5-len(jogadores_fracos)])
    
    # Pega os 5 piores
    piores_jogadores = jogadores_fracos[:5]
    # Embaralha para distribuição aleatória entre os times
    random.shuffle(piores_jogadores)
    
    # Pega os 5 melhores jogadores (do final da lista ordenada crescente)
    melhores_jogadores = jogadores_ordenados[-5:]
    # Embaralha para distribuição aleatória entre os times
    random.shuffle(melhores_jogadores)
    
    # Remove os piores e melhores jogadores da lista principal
    jogadores_restantes = [j for j in jogadores_ordenados if j not in piores_jogadores and j not in melhores_jogadores]
    
    # Agrupa os jogadores restantes por estrelas
    grupos = {}
    for jogador in jogadores_restantes:
        estrelas = jogador['habilidade']
        if estrelas not in grupos:
            grupos[estrelas] = []
        grupos[estrelas].append(jogador)
    
    # Ordena os grupos por estrelas (decrescente)
    grupos_ordenados = dict(sorted(grupos.items(), reverse=True))
    
    # Lista para armazenar os pares de jogadores
    pares = []
    jogadores_usados = set()
    
    # Dicionário para controlar times com jogadores < 3 estrelas
    times_com_jogador_fraco = {i: False for i in range(5)}
    
    # Para cada time (5 no total), começamos com os jogadores fracos
    for i in range(5):
        # Pega o pior jogador deste time
        pior_jogador = None
        
        # Se existem jogadores com habilidade < 3, tentamos distribuí-los uniformemente
        if jogadores_fracos_3:
            # Se ainda temos jogadores < 3 estrelas, distribuímos um por time
            jogadores_menores_3 = [j for j in piores_jogadores if j['habilidade'] < 3 and j['nome'] not in jogadores_usados]
            
            if jogadores_menores_3:
                pior_jogador = jogadores_menores_3[0]
                times_com_jogador_fraco[i] = True
            else:
                # Se não temos jogadores < 3 que não foram usados, pegamos qualquer jogador dos piores
                jogadores_disponiveis = [j for j in piores_jogadores if j['nome'] not in jogadores_usados]
                if jogadores_disponiveis:
                    pior_jogador = jogadores_disponiveis[0]
        else:
            # Se não temos jogadores < 3 estrelas, seguimos com a distribuição normal
            jogadores_disponiveis = [j for j in piores_jogadores if j['nome'] not in jogadores_usados]
            if jogadores_disponiveis:
                pior_jogador = jogadores_disponiveis[0]
        
        if pior_jogador:
            jogadores_usados.add(pior_jogador['nome'])
            
            # Pega o melhor jogador disponível para este time
            melhor_jogador = next((j for j in melhores_jogadores if j['nome'] not in jogadores_usados), None)
            if melhor_jogador:
                jogadores_usados.add(melhor_jogador['nome'])
                
                # Adiciona o par à lista
                pares.append((melhor_jogador, pior_jogador))
    
    # Se não conseguimos distribuir todos os pares, é porque temos muitos jogadores < 3 estrelas
    # ou alguma outra restrição não pôde ser satisfeita. Nesse caso, distribuímos os restantes
    if len(pares) < 5:
        # Jogadores não usados
        piores_restantes = [j for j in piores_jogadores if j['nome'] not in jogadores_usados]
        melhores_restantes = [j for j in melhores_jogadores if j['nome'] not in jogadores_usados]
        
        # Completamos os pares faltantes
        for i in range(len(pares), 5):
            if piores_restantes and melhores_restantes:
                pior_jogador = piores_restantes.pop(0)
                melhor_jogador = melhores_restantes.pop(0)
                pares.append((melhor_jogador, pior_jogador))
                print(f"ATENÇÃO: Não foi possível evitar que o Time {i+1} tenha mais de um jogador com nota < 3")
    
    return pares

def listar_jogadores_por_estrelas():
    # Carrega os jogadores do banco de dados
    jogadores = carregar_jogadores()
    
    # Criando dicionários para cada posição
    posicoes = {
        'zagueiros': {'primaria': [], 'versateis': []},
        'meias': {'primaria': [], 'versateis': []},
        'atacantes': {'primaria': [], 'versateis': []}
    }
    
    # Distribuindo jogadores nos dicionários
    for jogador in jogadores:
        posicao = jogador['posicao_primaria']
        if posicao == 'zagueiro':
            if jogador['posicao_secundaria'] == 'nenhum':
                posicoes['zagueiros']['primaria'].append(jogador)
            else:
                posicoes['zagueiros']['versateis'].append(jogador)
        elif posicao == 'meia':
            if jogador['posicao_secundaria'] == 'nenhum':
                posicoes['meias']['primaria'].append(jogador)
            else:
                posicoes['meias']['versateis'].append(jogador)
        elif posicao == 'atacante':
            if jogador['posicao_secundaria'] == 'nenhum':
                posicoes['atacantes']['primaria'].append(jogador)
            else:
                posicoes['atacantes']['versateis'].append(jogador)
    
    # Ordenando cada lista por habilidade antes do balanceamento
    for pos in posicoes:
        posicoes[pos]['primaria'].sort(key=lambda x: x['habilidade'], reverse=True)
        posicoes[pos]['versateis'].sort(key=lambda x: x['habilidade'], reverse=True)
    
    # Balancear as posições
    balancear_posicoes(posicoes)
    
    # Combinar e ordenar todos os jogadores por posição
    todos_zagueiros = posicoes['zagueiros']['primaria'] + posicoes['zagueiros']['versateis']
    todos_meias = posicoes['meias']['primaria'] + posicoes['meias']['versateis']
    todos_atacantes = posicoes['atacantes']['primaria'] + posicoes['atacantes']['versateis']
    
    # Ordenar novamente após o balanceamento
    todos_zagueiros.sort(key=lambda x: x['habilidade'], reverse=True)
    todos_meias.sort(key=lambda x: x['habilidade'], reverse=True)
    todos_atacantes.sort(key=lambda x: x['habilidade'], reverse=True)
    
    # Contagem total de jogadores para sorteio
    total_jogadores_validos = sum(1 for j in todos_zagueiros + todos_meias + todos_atacantes if j['nome'] != "")
    
    # Calcula a média das diferenças antes de mostrar os times
    media_diferencas = calcular_media_diferencas(executar_sorteio=False)
    
    # === CONTEÚDO DOS DICIONÁRIOS ===
    print("\n" + "="*80)
    print(" "*30 + "CONTEÚDO DOS DICIONÁRIOS")
    print("="*80)
    
    # Imprimindo conteúdo do dicionário de zagueiros
    print("\n" + "-"*35 + " DICIONÁRIO ZAGUEIROS " + "-"*35)
    print("\nPosição Primária:")
    print("Nome                  Estrelas")
    print("-" * 50)
    
    # Combinar e ordenar todos os zagueiros
    grupos_zagueiros = agrupar_por_estrelas(todos_zagueiros)
    
    contador = 1  # Contador contínuo para zagueiros
    for estrelas, jogadores in grupos_zagueiros.items():
        print(f"\n=== {estrelas} ESTRELAS ===")
        for jogador in jogadores:
            nome = jogador['nome'].ljust(20)
            pos_sec = f"        {jogador['posicao_secundaria'].capitalize()}" if jogador['posicao_secundaria'] != 'nenhum' else ''
            print(f"Zagueiro {str(contador).rjust(2)}: {nome} {str(estrelas).ljust(8)}{pos_sec}")
            contador += 1
    
    if len(todos_zagueiros) < 10:
        print("\n" + "-"*20)  # Linha divisória antes dos espaços vazios
        for i in range(len(todos_zagueiros) + 1, 11):
            print(f"Zagueiro {str(i).rjust(2)}: ")
    
    # Imprimindo conteúdo do dicionário de meias
    print("\n" + "-"*35 + " DICIONÁRIO MEIAS " + "-"*35)
    print("\nPosição Primária:")
    print("Nome                  Estrelas")
    print("-" * 50)
    
    # Combinar e ordenar todos os meias
    grupos_meias = agrupar_por_estrelas(todos_meias)
    
    contador = 1  # Contador contínuo para meias
    for estrelas, jogadores in grupos_meias.items():
        print(f"\n=== {estrelas} ESTRELAS ===")
        for jogador in jogadores:
            nome = jogador['nome'].ljust(20)
            pos_sec = f"        {jogador['posicao_secundaria'].capitalize()}" if jogador['posicao_secundaria'] != 'nenhum' else ''
            print(f"Meia {str(contador).rjust(2)}: {nome} {str(estrelas).ljust(8)}{pos_sec}")
            contador += 1
    
    if len(todos_meias) < 10:
        print("\n" + "-"*20)  # Linha divisória antes dos espaços vazios
        for i in range(len(todos_meias) + 1, 11):
            print(f"Meia {str(i).rjust(2)}: ")
    
    # Imprimindo conteúdo do dicionário de atacantes
    print("\n" + "-"*35 + " DICIONÁRIO ATACANTES " + "-"*35)
    print("\nPosição Primária:")
    print("Nome                  Estrelas")
    print("-" * 50)
    
    # Combinar e ordenar todos os atacantes
    grupos_atacantes = agrupar_por_estrelas(todos_atacantes)
    
    contador = 1  # Contador contínuo para atacantes
    for estrelas, jogadores in grupos_atacantes.items():
        print(f"\n=== {estrelas} ESTRELAS ===")
        for jogador in jogadores:
            nome = jogador['nome'].ljust(20)
            pos_sec = f"        {jogador['posicao_secundaria'].capitalize()}" if jogador['posicao_secundaria'] != 'nenhum' else ''
            print(f"Atacante {str(contador).rjust(2)}: {nome} {str(estrelas).ljust(8)}{pos_sec}")
            contador += 1
    
    if len(todos_atacantes) < 10:
        print("\n" + "-"*20)  # Linha divisória antes dos espaços vazios
        for i in range(len(todos_atacantes) + 1, 11):
            print(f"Atacante {str(i).rjust(2)}: ")
    
    # === TIMES ===
    print("\n=== TIMES ===")
    
    # Cria 5 times vazios
    times = {
        "Time 1": {"zagueiros": [], "meias": [], "atacantes": [], "jogadores_fracos": 0},
        "Time 2": {"zagueiros": [], "meias": [], "atacantes": [], "jogadores_fracos": 0},
        "Time 3": {"zagueiros": [], "meias": [], "atacantes": [], "jogadores_fracos": 0},
        "Time 4": {"zagueiros": [], "meias": [], "atacantes": [], "jogadores_fracos": 0},
        "Time 5": {"zagueiros": [], "meias": [], "atacantes": [], "jogadores_fracos": 0}
    }
    
    # Lista para rastrear jogadores com nota < 3
    jogadores_fracos_distribuidos = []
    
    # Para cada posição, distribui os jogadores nos times
    for posicao, jogadores_lista in [('zagueiros', todos_zagueiros), ('meias', todos_meias), ('atacantes', todos_atacantes)]:
        # Certifica-se de que temos 10 jogadores
        while len(jogadores_lista) < 10:
            # Adiciona jogadores vazios se necessário
            jogadores_lista.append({"nome": "", "habilidade": 0, "posicao_primaria": posicao[:-1], "posicao_secundaria": "nenhum"})
            print(f"ATENÇÃO: Adicionado jogador vazio para a posição {posicao} (total agora: {len(jogadores_lista)})")
        
        # Identifica jogadores com nota < 3
        jogadores_fracos = [j for j in jogadores_lista if j['habilidade'] < 3 and j['nome'] != ""]
        
        # Cria uma cópia da lista de jogadores_lista para trabalhar
        jogadores_para_distribuir = jogadores_lista.copy()
        
        # Distribui primeiro os jogadores fracos em times diferentes
        for jogador in jogadores_fracos:
            # Remove o jogador da lista de jogadores para distribuir
            jogadores_para_distribuir.remove(jogador)
            
            # Procura um time com menos jogadores fracos
            times_ordenados = sorted(times.keys(), key=lambda t: times[t]["jogadores_fracos"])
            
            for time_nome in times_ordenados:
                # Verifica se este time já tem jogadores fracos nesta mesma posição
                if any(j['habilidade'] < 3 for j in times[time_nome][posicao]):
                    continue
                
                # Adiciona o jogador fraco ao time
                times[time_nome][posicao].append(jogador)
                times[time_nome]["jogadores_fracos"] += 1
                jogadores_fracos_distribuidos.append(jogador)
                print(f"Jogador fraco: {jogador['nome']} ({jogador['habilidade']} estrelas) adicionado ao {time_nome}")
                break
            else:
                # Se não conseguiu distribuir, adiciona ao time com menos jogadores fracos
                time_nome = times_ordenados[0]
                times[time_nome][posicao].append(jogador)
                times[time_nome]["jogadores_fracos"] += 1
                jogadores_fracos_distribuidos.append(jogador)
                print(f"ATENÇÃO: Não foi possível evitar times com múltiplos jogadores fracos. {jogador['nome']} adicionado ao {time_nome}")
        
        # Ordena os jogadores restantes por habilidade (do maior para o menor)
        jogadores_para_distribuir.sort(key=lambda x: x['habilidade'], reverse=True)
        
        # Distribui os jogadores bons restantes, priorizando balancear times
        while jogadores_para_distribuir:
            # Verifica quais times ainda precisam de jogadores nesta posição
            times_incompletos = [nome for nome, time in times.items() if len(time[posicao]) < 2]
            
            if not times_incompletos:
                break  # Todos os times já têm 2 jogadores nesta posição
            
            # Ordena os times incompletos pelo número de jogadores fracos (decrescente) e depois pela soma de habilidades (crescente)
            def chave_ordenacao(time_nome):
                jogadores_posicao = times[time_nome][posicao]
                soma_habilidades = sum(j['habilidade'] for j in jogadores_posicao)
                return (soma_habilidades,)  # Apenas pela soma de habilidades (crescente)
            
            # Ordena os times incompletos
            times_incompletos.sort(key=chave_ordenacao)
            
            # Pega o próximo time que precisa de jogador
            time_alvo = times_incompletos[0]
            
            # Pega o melhor jogador disponível
            jogador = jogadores_para_distribuir.pop(0)
            
            # Adiciona ao time
            times[time_alvo][posicao].append(jogador)
    
    # Remove o contador de jogadores fracos antes de imprimir
    for time in times.values():
        time.pop("jogadores_fracos", None)
    
    # Embaralha os times para que os números sejam aleatórios
    times_lista = list(times.items())
    random.shuffle(times_lista)
    
    # Cria novos times com números embaralhados
    times_embaralhados = {}
    for i, (_, time_dados) in enumerate(times_lista, 1):
        times_embaralhados[f"Time {i}"] = time_dados
    
    # Imprime cada time
    print("\nTimes Sorteados\n")
    
    # Lista para armazenar o total de estrelas de cada time
    totais_estrelas = []
    
    for nome_time, posicoes_time in times_embaralhados.items():
        print(f"--------------- {nome_time} ---------------")
        
        # Calcula o total de estrelas do time
        total_estrelas = 0
        todos_jogadores = []
        
        # Coleta todos os jogadores do time
        for posicao in ["zagueiros", "meias", "atacantes"]:
            for jogador in posicoes_time[posicao]:
                if jogador["nome"]:  # Se não for um jogador vazio
                    total_estrelas += jogador['habilidade']
                    todos_jogadores.append(jogador)
        
        # Armazena o total de estrelas deste time
        totais_estrelas.append(total_estrelas)
        
        # Conta as posições primárias
        posicoes_primarias = {"zagueiro": 0, "meia": 0, "atacante": 0}
        posicoes_secundarias = {"zagueiro": 0, "meia": 0, "atacante": 0}
        
        for jogador in todos_jogadores:
            if jogador["nome"]:
                posicoes_primarias[jogador['posicao_primaria']] += 1
                if jogador['posicao_secundaria'] != 'nenhum':
                    posicoes_secundarias[jogador['posicao_secundaria']] += 1
        
        # Imprime cabeçalho do time
        print(f"{nome_time} | {total_estrelas:.1f} Estrelas")
        print(f"1° Posição: {posicoes_primarias['zagueiro']} Zag, {posicoes_primarias['meia']} Mei, {posicoes_primarias['atacante']} Ata")
        
        # Se houver jogadores com posição secundária, imprime a linha
        if sum(posicoes_secundarias.values()) > 0:
            print(f"2° Posição: {posicoes_secundarias['zagueiro']} Zag, {posicoes_secundarias['meia']} Mei, {posicoes_secundarias['atacante']} Ata")
        
        print("")
        
        # Lista para armazenar todos os jogadores do time por posição
        todos_jogadores_por_posicao = []
        
        # Organizar jogadores por posição
        for posicao in ["zagueiros", "meias", "atacantes"]:
            # Filtra jogadores desta posição
            jogadores_posicao = []
            for jogador in posicoes_time[posicao]:
                if jogador["nome"]:  # Se não for um jogador vazio
                    jogadores_posicao.append(jogador)
            
            # Se tiver jogadores nessa posição
            if jogadores_posicao:
                # Ordena por estrelas (decrescente)
                jogadores_posicao.sort(key=lambda x: (-x['habilidade'], x['nome']))
                
                # Adiciona os jogadores à lista geral, com sua posição
                for jogador in jogadores_posicao:
                    pos_no_time = ""
                    if posicao == "zagueiros":
                        pos_no_time = "Zag"
                    elif posicao == "meias":
                        pos_no_time = "Mei"
                    elif posicao == "atacantes":
                        pos_no_time = "Ata"
                    
                    todos_jogadores_por_posicao.append((jogador, pos_no_time))
        
        # Imprime todos os jogadores do time
        for jogador, pos_no_time in todos_jogadores_por_posicao:
            nome = jogador['nome']
            estrelas = jogador['habilidade']
            print(f"{nome} | {estrelas} Estrelas | {pos_no_time}")
        
        print("")
    
    # Exibe o total de jogadores para sorteio
    print(f"\nTotal de jogadores para sorteio: {total_jogadores_validos}")
    
    # Imprime o intervalo de estrelas (min - max)
    min_estrelas = min(totais_estrelas)
    max_estrelas = max(totais_estrelas)
    diferenca = max_estrelas - min_estrelas
    print(f"{min_estrelas:.1f} - {max_estrelas:.1f} | Diferença: {diferenca:.1f} | Média: {media_diferencas:.1f}")
    
    # Perguntar se deseja salvar o sorteio
    resposta = input("\nDeseja salvar este sorteio? (s/n): ")
    if resposta.lower() == 's':
        salvar_sorteio(times_embaralhados, totais_estrelas, total_jogadores_validos, min_estrelas, max_estrelas, diferenca, media_diferencas)

def salvar_sorteio(times, totais_estrelas, total_jogadores, min_estrelas, max_estrelas, diferenca, media_diferencas):
    """
    Salva o resultado do sorteio em um arquivo de texto na pasta 'resultados'.
    """
    # Cria a pasta 'resultados' se não existir
    pasta_resultados = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"sorteio_{timestamp}.txt"
    caminho_arquivo = os.path.join(pasta_resultados, nome_arquivo)
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write("="*50 + "\n")
        arquivo.write(" "*15 + "RESULTADO DO SORTEIO\n")
        arquivo.write("="*50 + "\n\n")
        
        arquivo.write(f"Total de jogadores para sorteio: {total_jogadores}\n")
        arquivo.write(f"Diferença de estrelas: {min_estrelas:.1f} - {max_estrelas:.1f} | Diferença: {diferenca:.1f} | Média: {media_diferencas:.1f}\n\n")
        
        for nome_time, posicoes_time in times.items():
            arquivo.write(f"--------------- {nome_time} ---------------\n")
            
            # Calcula o total de estrelas do time
            total_estrelas = 0
            todos_jogadores = []
            
            # Coleta todos os jogadores do time
            for posicao in ["zagueiros", "meias", "atacantes"]:
                for jogador in posicoes_time[posicao]:
                    if jogador["nome"]:  # Se não for um jogador vazio
                        total_estrelas += jogador['habilidade']
                        todos_jogadores.append(jogador)
            
            # Conta as posições primárias
            posicoes_primarias = {"zagueiro": 0, "meia": 0, "atacante": 0}
            posicoes_secundarias = {"zagueiro": 0, "meia": 0, "atacante": 0}
            
            for jogador in todos_jogadores:
                if jogador["nome"]:
                    posicoes_primarias[jogador['posicao_primaria']] += 1
                    if jogador['posicao_secundaria'] != 'nenhum':
                        posicoes_secundarias[jogador['posicao_secundaria']] += 1
            
            # Escreve cabeçalho do time
            arquivo.write(f"{nome_time} | {total_estrelas:.1f} Estrelas\n")
            arquivo.write(f"1° Posição: {posicoes_primarias['zagueiro']} Zag, {posicoes_primarias['meia']} Mei, {posicoes_primarias['atacante']} Ata\n")
            
            # Se houver jogadores com posição secundária, escreve a linha
            if sum(posicoes_secundarias.values()) > 0:
                arquivo.write(f"2° Posição: {posicoes_secundarias['zagueiro']} Zag, {posicoes_secundarias['meia']} Mei, {posicoes_secundarias['atacante']} Ata\n")
            
            arquivo.write("\n")
            
            # Lista para armazenar todos os jogadores do time por posição
            todos_jogadores_por_posicao = []
            
            # Organizar jogadores por posição
            for posicao in ["zagueiros", "meias", "atacantes"]:
                # Filtra jogadores desta posição
                jogadores_posicao = []
                for jogador in posicoes_time[posicao]:
                    if jogador["nome"]:  # Se não for um jogador vazio
                        jogadores_posicao.append(jogador)
                
                # Se tiver jogadores nessa posição
                if jogadores_posicao:
                    # Ordena por estrelas (decrescente)
                    jogadores_posicao.sort(key=lambda x: (-x['habilidade'], x['nome']))
                    
                    # Adiciona os jogadores à lista geral, com sua posição
                    for jogador in jogadores_posicao:
                        pos_no_time = ""
                        if posicao == "zagueiros":
                            pos_no_time = "Zag"
                        elif posicao == "meias":
                            pos_no_time = "Mei"
                        elif posicao == "atacantes":
                            pos_no_time = "Ata"
                        
                        todos_jogadores_por_posicao.append((jogador, pos_no_time))
            
            # Escreve todos os jogadores do time
            for jogador, pos_no_time in todos_jogadores_por_posicao:
                nome = jogador['nome']
                estrelas = jogador['habilidade']
                arquivo.write(f"{nome} | {estrelas} Estrelas | {pos_no_time}\n")
            
            arquivo.write("\n")
    
    print(f"Sorteio salvo em: {caminho_arquivo}")

def calcular_media_diferencas(executar_sorteio=True, num_sorteios=10):
    """
    Executa vários sorteios e calcula a média das diferenças entre o time com mais estrelas
    e o time com menos estrelas.
    
    Parâmetros:
    - executar_sorteio: se True, mostra o progresso de cada sorteio
    - num_sorteios: número de sorteios a executar
    
    Retorna a média das diferenças.
    """
    if executar_sorteio:
        print(f"\nCalculando média de {num_sorteios} sorteios...")
        
    diferencas = []
    
    # Redirecionar a saída padrão se não quisermos mostrar o progresso
    if not executar_sorteio:
        saida_original = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    
    for i in range(num_sorteios):
        # Carrega os jogadores do banco de dados
        jogadores = carregar_jogadores()
        
        # Criando dicionários para cada posição
        posicoes = {
            'zagueiros': {'primaria': [], 'versateis': []},
            'meias': {'primaria': [], 'versateis': []},
            'atacantes': {'primaria': [], 'versateis': []}
        }
        
        # Distribuindo jogadores nos dicionários
        for jogador in jogadores:
            posicao = jogador['posicao_primaria']
            if posicao == 'zagueiro':
                if jogador['posicao_secundaria'] == 'nenhum':
                    posicoes['zagueiros']['primaria'].append(jogador)
                else:
                    posicoes['zagueiros']['versateis'].append(jogador)
            elif posicao == 'meia':
                if jogador['posicao_secundaria'] == 'nenhum':
                    posicoes['meias']['primaria'].append(jogador)
                else:
                    posicoes['meias']['versateis'].append(jogador)
            elif posicao == 'atacante':
                if jogador['posicao_secundaria'] == 'nenhum':
                    posicoes['atacantes']['primaria'].append(jogador)
                else:
                    posicoes['atacantes']['versateis'].append(jogador)
        
        # Ordenando cada lista por habilidade
        for pos in posicoes:
            posicoes[pos]['primaria'].sort(key=lambda x: x['habilidade'], reverse=True)
            posicoes[pos]['versateis'].sort(key=lambda x: x['habilidade'], reverse=True)
        
        # Combinar e ordenar todos os jogadores por posição
        todos_zagueiros = posicoes['zagueiros']['primaria'] + posicoes['zagueiros']['versateis']
        todos_meias = posicoes['meias']['primaria'] + posicoes['meias']['versateis']
        todos_atacantes = posicoes['atacantes']['primaria'] + posicoes['atacantes']['versateis']
        
        # Ordenar novamente
        todos_zagueiros.sort(key=lambda x: x['habilidade'], reverse=True)
        todos_meias.sort(key=lambda x: x['habilidade'], reverse=True)
        todos_atacantes.sort(key=lambda x: x['habilidade'], reverse=True)
        
        # Cria 5 times vazios
        times = {
            "Time 1": {"zagueiros": [], "meias": [], "atacantes": [], "jogadores_fracos": 0},
            "Time 2": {"zagueiros": [], "meias": [], "atacantes": [], "jogadores_fracos": 0},
            "Time 3": {"zagueiros": [], "meias": [], "atacantes": [], "jogadores_fracos": 0},
            "Time 4": {"zagueiros": [], "meias": [], "atacantes": [], "jogadores_fracos": 0},
            "Time 5": {"zagueiros": [], "meias": [], "atacantes": [], "jogadores_fracos": 0}
        }
        
        # Lista para rastrear jogadores com nota < 3
        jogadores_fracos_distribuidos = []
        
        # Para cada posição, distribui os jogadores nos times
        for posicao, jogadores_lista in [('zagueiros', todos_zagueiros), ('meias', todos_meias), ('atacantes', todos_atacantes)]:
            # Certifica-se de que temos 10 jogadores
            while len(jogadores_lista) < 10:
                # Adiciona jogadores vazios se necessário
                jogadores_lista.append({"nome": "", "habilidade": 0, "posicao_primaria": posicao[:-1], "posicao_secundaria": "nenhum"})
            
            # Identifica jogadores com nota < 3
            jogadores_fracos = [j for j in jogadores_lista if j['habilidade'] < 3 and j['nome'] != ""]
            
            # Cria uma cópia da lista de jogadores_lista para trabalhar
            jogadores_para_distribuir = jogadores_lista.copy()
            
            # Distribui primeiro os jogadores fracos em times diferentes
            for jogador in jogadores_fracos:
                # Remove o jogador da lista de jogadores para distribuir
                jogadores_para_distribuir.remove(jogador)
                
                # Procura um time com menos jogadores fracos
                times_ordenados = sorted(times.keys(), key=lambda t: times[t]["jogadores_fracos"])
                
                for time_nome in times_ordenados:
                    # Verifica se este time já tem jogadores fracos nesta mesma posição
                    if any(j['habilidade'] < 3 for j in times[time_nome][posicao]):
                        continue
                    
                    # Adiciona o jogador fraco ao time
                    times[time_nome][posicao].append(jogador)
                    times[time_nome]["jogadores_fracos"] += 1
                    jogadores_fracos_distribuidos.append(jogador)
                    break
                else:
                    # Se não conseguiu distribuir, adiciona ao time com menos jogadores fracos
                    time_nome = times_ordenados[0]
                    times[time_nome][posicao].append(jogador)
                    times[time_nome]["jogadores_fracos"] += 1
                    jogadores_fracos_distribuidos.append(jogador)
            
            # Ordena os jogadores restantes por habilidade (do maior para o menor)
            jogadores_para_distribuir.sort(key=lambda x: x['habilidade'], reverse=True)
            
            # Distribui os jogadores bons restantes, priorizando balancear times
            while jogadores_para_distribuir:
                # Verifica quais times ainda precisam de jogadores nesta posição
                times_incompletos = [nome for nome, time in times.items() if len(time[posicao]) < 2]
                
                if not times_incompletos:
                    break  # Todos os times já têm 2 jogadores nesta posição
                
                # Ordena os times incompletos pelo número de jogadores fracos (decrescente) e depois pela soma de habilidades (crescente)
                def chave_ordenacao(time_nome):
                    jogadores_posicao = times[time_nome][posicao]
                    soma_habilidades = sum(j['habilidade'] for j in jogadores_posicao)
                    return (soma_habilidades,)  # Apenas pela soma de habilidades (crescente)
                
                # Ordena os times incompletos
                times_incompletos.sort(key=chave_ordenacao)
                
                # Pega o próximo time que precisa de jogador
                time_alvo = times_incompletos[0]
                
                # Pega o melhor jogador disponível
                jogador = jogadores_para_distribuir.pop(0)
                
                # Adiciona ao time
                times[time_alvo][posicao].append(jogador)
        
        # Remove o contador de jogadores fracos antes de calcular
        for time in times.values():
            time.pop("jogadores_fracos", None)
        
        # Calcular total de estrelas de cada time
        totais_estrelas = []
        for posicoes_time in times.values():
            total_estrelas = 0
            for posicao in ["zagueiros", "meias", "atacantes"]:
                for jogador in posicoes_time[posicao]:
                    if jogador["nome"]:  # Se não for um jogador vazio
                        total_estrelas += jogador['habilidade']
            totais_estrelas.append(total_estrelas)
        
        # Calcular diferença para este sorteio
        min_estrelas = min(totais_estrelas)
        max_estrelas = max(totais_estrelas)
        diferenca = max_estrelas - min_estrelas
        diferencas.append(diferenca)
        
        if executar_sorteio:
            print(f"Sorteio {i+1}: {min_estrelas:.1f} - {max_estrelas:.1f} | Diferença: {diferenca:.1f}")
    
    # Restaurar a saída padrão
    if not executar_sorteio:
        sys.stdout = saida_original
    
    # Calcular média das diferenças
    media = sum(diferencas) / len(diferencas)
    
    if executar_sorteio:
        print(f"\nResultado dos {num_sorteios} sorteios:")
        print(f"Média das diferenças: {media:.1f}")
    
    # Retornar a média para uso posterior
    return media

if __name__ == "__main__":
    listar_jogadores_por_estrelas()