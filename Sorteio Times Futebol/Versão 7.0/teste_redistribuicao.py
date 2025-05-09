import unicodedata
import json
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

# Lista de jogadores simplificada para teste
lista_jogadores = [
    # ZAGUEIROS (8)
    {"nome": "Claudino", "habilidade": 4.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "nenhum"},
    {"nome": "João Vitor", "habilidade": 4, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Betinho", "habilidade": 3.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Léo A.", "habilidade": 3.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "nenhum"},
    {"nome": "Thiago Sultanum", "habilidade": 3.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "nenhum"},
    {"nome": "Lázaro", "habilidade": 3.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Alysson Pink", "habilidade": 3, "posicao_primaria": "zagueiro", "posicao_secundaria": "nenhum"},
    {"nome": "Sérgio Falcão", "habilidade": 2.5, "posicao_primaria": "zagueiro", "posicao_secundaria": "atacante"},
    
    # MEIAS (9)
    {"nome": "Diego Rocha", "habilidade": 4.5, "posicao_primaria": "meia", "posicao_secundaria": "zagueiro"},
    {"nome": "Felipe Pita", "habilidade": 4.5, "posicao_primaria": "meia", "posicao_secundaria": "zagueiro"},
    {"nome": "Kiel", "habilidade": 4, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Paulo Thiago", "habilidade": 4, "posicao_primaria": "meia", "posicao_secundaria": "zagueiro"},
    {"nome": "Thayan", "habilidade": 4, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Bidu", "habilidade": 3.5, "posicao_primaria": "meia", "posicao_secundaria": "zagueiro"},
    {"nome": "Dato", "habilidade": 3.5, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Goncalves", "habilidade": 3.5, "posicao_primaria": "meia", "posicao_secundaria": "zagueiro"},
    {"nome": "Flavio Ureia", "habilidade": 3.5, "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    
    # ATACANTES (13)
    {"nome": "Bruno Pessoa", "habilidade": 4.5, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"},
    {"nome": "Jackson", "habilidade": 4.5, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Manga", "habilidade": 4.5, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Cadu", "habilidade": 4.5, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Marcos S.", "habilidade": 3.5, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Lucas H.", "habilidade": 3, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Nagibio", "habilidade": 3, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"},
    {"nome": "Rafa Ribeiro", "habilidade": 3, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Hiago", "habilidade": 3, "posicao_primaria": "atacante", "posicao_secundaria": "meia"},
    {"nome": "Teixa", "habilidade": 2.5, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"},
    {"nome": "Lucas S.", "habilidade": 2, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"},
    {"nome": "Thiago Alemão", "habilidade": 2, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"},
    {"nome": "Xandinho", "habilidade": 2, "posicao_primaria": "atacante", "posicao_secundaria": "nenhum"}
]

# Configurações
POSICOES = ['ZAGUEIROS', 'MEIAS', 'ATACANTES']
MAPA_POSICOES = {'zagueiro': 'ZAGUEIROS', 'meia': 'MEIAS', 'atacante': 'ATACANTES'}
NUM_TIMES = 5

# Inicializar times
times = {pos: [] for pos in POSICOES}
for jogador in lista_jogadores:
    if pos := MAPA_POSICOES.get(jogador['posicao_primaria']):
        times[pos].append(jogador)

# Ordenar por habilidade
for pos in times:
    times[pos].sort(key=lambda j: j['habilidade'], reverse=True)

# Função para imprimir lista de jogadores
def imprimir_lista_jogadores(times, titulo):
    """Imprime a lista de jogadores formatada"""
    print("\n" + "="*80)
    print(remover_acentos(titulo).center(80))
    print("="*80)

    print("\nLISTA DE JOGADORES:")
    print("-"*80)
    print(f"{'ZAGUEIROS':<30} {'MEIAS':<30} {'ATACANTES':<30}")
    print("-"*80)

    from itertools import zip_longest
    for i, row in enumerate(zip_longest(*[times[pos] for pos in POSICOES], fillvalue=None), 1):
        linha = []
        for jogador in row:
            if jogador:
                pos_sec = '-' if jogador['posicao_secundaria'] == 'nenhum' else jogador['posicao_secundaria']
                nome_sem_acento = remover_acentos(jogador['nome'])
                linha.append(f"{i}- {nome_sem_acento} ({jogador['habilidade']}) [{pos_sec}]")
            else:
                linha.append("")
        print(f"{linha[0]:<30} {linha[1]:<30} {linha[2] if len(linha) > 2 else ''}")

    print("-"*80)

# Imprimir lista inicial
imprimir_lista_jogadores(times, "JOGADORES POR POSIÇÃO (INICIAL)")

# Função para redistribuir jogadores
def redistribuir_jogadores(times):
    """Redistribui jogadores para balancear os times"""
    # Análise inicial da quantidade de jogadores
    print("\nANÁLISE INICIAL DA DISTRIBUIÇÃO:")
    print("-"*50)
    for pos in POSICOES:
        qtd = len(times[pos])
        print(f"{pos}: {qtd} jogadores")
    print("-"*50)
    
    # Função para mover jogador
    def mover_jogador(jogador, origem, destino, motivo="POSIÇÃO SECUNDÁRIA"):
        times[origem].remove(jogador)
        times[destino].append(jogador)
        times[origem].sort(key=lambda j: j['habilidade'], reverse=True)
        times[destino].sort(key=lambda j: j['habilidade'], reverse=True)
        nome = remover_acentos(jogador['nome'])
        motivo = remover_acentos(motivo)
        print(f"MOVENDO POR {motivo}: {nome} ({jogador['habilidade']}) de {origem} para {destino}")
    
    # Quantos jogadores precisamos em cada posição
    jogadores_por_posicao = 10
    
    # Calcular quantos precisamos mover para cada posição
    mover_para_zagueiros = max(0, jogadores_por_posicao - len(times['ZAGUEIROS']))
    mover_para_meias = max(0, jogadores_por_posicao - len(times['MEIAS']))
    mover_para_atacantes = max(0, jogadores_por_posicao - len(times['ATACANTES']))
    
    print(f"\nPrecisamos de mais {mover_para_zagueiros} zagueiros, {mover_para_meias} meias e {mover_para_atacantes} atacantes")
    
    # ETAPA 1: Mover meias com posição secundária zagueiro para zagueiros
    if mover_para_zagueiros > 0:
        print("\n--- ETAPA 1: MOVENDO MEIAS QUE JOGAM DE ZAGUEIRO ---")
        
        # Encontrar meias que jogam de zagueiro
        meias_zagueiros = []
        for jogador in times['MEIAS']:
            if jogador['posicao_secundaria'] == 'zagueiro':
                meias_zagueiros.append(jogador)
        
        # Ordenar por habilidade (maiores primeiro)
        meias_zagueiros.sort(key=lambda j: j['habilidade'], reverse=True)
        
        print(f"Encontrados {len(meias_zagueiros)} meias que jogam de zagueiro")
        
        # Mover os necessários
        for i in range(min(len(meias_zagueiros), mover_para_zagueiros)):
            mover_jogador(meias_zagueiros[i], 'MEIAS', 'ZAGUEIROS', "MEIA QUE JOGA ZAGUEIRO")
            mover_para_zagueiros -= 1
    
    # ETAPA 2: Mover atacantes com posição secundária meia para meias
    # Recalcular quanto precisamos de cada
    mover_para_meias = max(0, jogadores_por_posicao - len(times['MEIAS']))
    
    if mover_para_meias > 0:
        print("\n--- ETAPA 2: MOVENDO ATACANTES QUE JOGAM DE MEIA ---")
        
        # Encontrar atacantes que jogam de meia
        atacantes_meias = []
        for jogador in times['ATACANTES']:
            if jogador['posicao_secundaria'] == 'meia':
                atacantes_meias.append(jogador)
        
        # Ordenar por habilidade (maiores primeiro)
        atacantes_meias.sort(key=lambda j: j['habilidade'], reverse=True)
        
        print(f"Encontrados {len(atacantes_meias)} atacantes que jogam de meia")
        
        # Mover os necessários
        for i in range(min(len(atacantes_meias), mover_para_meias)):
            mover_jogador(atacantes_meias[i], 'ATACANTES', 'MEIAS', "ATACANTE QUE JOGA MEIA")
            mover_para_meias -= 1
    
    # ETAPA 3: Usar coringas (jogadores sem posição secundária)
    # Recalcular quanto precisamos de cada
    mover_para_zagueiros = max(0, jogadores_por_posicao - len(times['ZAGUEIROS']))
    mover_para_meias = max(0, jogadores_por_posicao - len(times['MEIAS']))
    
    if mover_para_zagueiros > 0 or mover_para_meias > 0:
        print("\n--- ETAPA 3: USANDO CORINGAS ---")
        
        # Para zagueiros que faltam, usar atacantes como coringa
        if mover_para_zagueiros > 0:
            print(f"Ainda precisamos de {mover_para_zagueiros} zagueiros")
            
            # Encontrar atacantes que podem ser usados como coringa
            atacantes_coringas = []
            for jogador in times['ATACANTES']:
                if jogador['posicao_secundaria'] == 'nenhum':
                    atacantes_coringas.append(jogador)
            
            # Ordenar por habilidade (maiores primeiro)
            atacantes_coringas.sort(key=lambda j: j['habilidade'], reverse=True)
            
            print(f"Encontrados {len(atacantes_coringas)} atacantes que podem ser coringas")
            
            # Mover os necessários
            for i in range(min(len(atacantes_coringas), mover_para_zagueiros)):
                mover_jogador(atacantes_coringas[i], 'ATACANTES', 'ZAGUEIROS', "CORINGA")
                mover_para_zagueiros -= 1
    
    # Análise final da quantidade de jogadores
    print("\nANÁLISE FINAL DA DISTRIBUIÇÃO:")
    print("-"*50)
    for pos in POSICOES:
        qtd = len(times[pos])
        print(f"{pos}: {qtd} jogadores")
    print("-"*50)
    
    return times

# Redistribuir jogadores
times = redistribuir_jogadores(times)

# Imprimir lista após redistribuição
imprimir_lista_jogadores(times, "JOGADORES POR POSIÇÃO (APÓS REDISTRIBUIÇÃO)") 