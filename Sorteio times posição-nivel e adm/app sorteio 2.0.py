import random

jogadores = [
    {"nome": "Albert", "habilidade": 5, "adm": True,
        "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Betinho", "habilidade": 4, "adm": True,
        "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Bidu", "habilidade": 4, "adm": False,
        "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Bruno Pessoa", "habilidade": 3.5, "adm": False,
        "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Dato", "habilidade": 4, "adm": False,
        "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Diego", "habilidade": 4, "adm": False,
        "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Eduardo", "habilidade": 4, "adm": False,
        "posicao_primaria": "zagueiro", "posicao_secundaria": "atacante"},
    {"nome": "Eric", "habilidade": 3.5, "adm": True,
        "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Flávio", "habilidade": 3.5, "adm": False,
        "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Henrique Silva", "habilidade": 4, "adm": False,
        "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Kiel", "habilidade": 5, "adm": False,
        "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Lucas Henrique", "habilidade": 3, "adm": False,
        "posicao_primaria": "atacante", "posicao_secundaria": None},
    {"nome": "Lucas Silveira", "habilidade": 1, "adm": False,
        "posicao_primaria": "atacante", "posicao_secundaria": None},
    {"nome": "Marcelinho", "habilidade": 4, "adm": False,
        "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Matheus Ureia", "habilidade": 4, "adm": False,
        "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Nicláudio Mello", "habilidade": 2.5, "adm": False,
        "posicao_primaria": "atacante", "posicao_secundaria": None},
    {"nome": "Raphael Borges", "habilidade": 4, "adm": False,
        "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Teixa", "habilidade": 2.5, "adm": False,
        "posicao_primaria": "atacante", "posicao_secundaria": "zagueiro"},
    {"nome": "Thiago Alemão", "habilidade": 1.5, "adm": False,
        "posicao_primaria": "atacante", "posicao_secundaria": None},
    {"nome": "Vinícius", "habilidade": 5, "adm": False,
        "posicao_primaria": "atacante", "posicao_secundaria": "zagueiro"},
    {"nome": "Jackson", "habilidade": 4, "adm": False,
        "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Sergio Falção", "habilidade": 2.5, "adm": False,
        "posicao_primaria": "zagueiro", "posicao_secundaria": "atacante"},
    {"nome": "Léo A.", "habilidade": 3, "adm": False,
        "posicao_primaria": "zagueiro", "posicao_secundaria": "meia"},
    {"nome": "Winnicius C.", "habilidade": 5, "adm": False,
        "posicao_primaria": "meia", "posicao_secundaria": "atacante"},
    {"nome": "Alysson Pink", "habilidade": 3, "adm": False,
        "posicao_primaria": "Qualquer", "posicao_secundaria": None}
]

# Função para criar times com base nas habilidade e posições dos jogadores


def criar_times(jogadores, num_times):
    # Fazer uma cópia aleatória da lista de jogadores
    jogadores_copia = random.sample(jogadores, len(jogadores))

    # Separar jogadores com 'adm': True e 'adm': False
    jogadores_adm_true = [j for j in jogadores_copia if j['adm']]
    jogadores_adm_false = [j for j in jogadores_copia if not j['adm']]

    # Ordenar ambos os grupos por habilidade de forma decrescente
    jogadores_adm_true = sorted(
        jogadores_adm_true, key=lambda x: x["habilidade"], reverse=True)
    jogadores_adm_false = sorted(
        jogadores_adm_false, key=lambda x: x["habilidade"], reverse=True)

    # Inicializa os times como listas vazias
    times = [[] for _ in range(num_times)]

    # Distribui jogadores com 'adm': True primeiro
    for jogador in jogadores_adm_true:
        # Encontra o time com menor número de jogadores e posições equilibradas
        menor_time = min(times, key=lambda t: (
            sum(j["habilidade"] for j in t), count_positions(t, jogador)))

        # Adiciona o jogador ao time
        menor_time.append(jogador)

        # Remove o jogador da lista geral apenas se não for "Qualquer"
        if jogador["posicao_primaria"] != "Qualquer":
            jogadores.remove(jogador)

        # Verifica se todos os jogadores foram distribuídos
        if not jogadores:
            break

    # Distribui os jogadores com 'adm': False
    for jogador in jogadores_adm_false:
        # Se a posição primária for "Qualquer", distribui o jogador em uma posição aleatória
        if jogador["posicao_primaria"] == "Qualquer":
            posicoes_possiveis = ["zagueiro", "meia", "atacante"]
            random.shuffle(posicoes_possiveis)
            for posicao in posicoes_possiveis:
                # Encontra o time com menor número de jogadores e posições equilibradas
                menor_time = min(times, key=lambda t: (
                    sum(j["habilidade"] for j in t), count_positions(t, jogador, posicao)))

                # Adiciona o jogador ao time
                menor_time.append(jogador)

                # Verifica se todos os jogadores foram distribuídos
                if not jogadores:
                    break
        else:
            # Encontra o time com menor número de jogadores e posições equilibradas
            menor_time = min(times, key=lambda t: (
                sum(j["habilidade"] for j in t), count_positions(t, jogador)))

            # Adiciona o jogador ao time
            menor_time.append(jogador)

            # Remove o jogador da lista geral apenas se não for "Qualquer"
            if jogador["posicao_primaria"] != "Qualquer":
                jogadores.remove(jogador)

            # Verifica se todos os jogadores foram distribuídos
            if not jogadores:
                break

    return times

# Função auxiliar para contar a quantidade de jogadores em cada posição


def count_positions(time, jogador, posicao=None):
    count_primarias = sum(
        1 for j in time if j["posicao_primaria"] == jogador["posicao_primaria"])
    count_secundarias = sum(
        1 for j in time if j["posicao_secundaria"] == jogador["posicao_secundaria"])

    if posicao:
        count_primarias += 1 if jogador["posicao_primaria"] == posicao else 0
        count_secundarias += 1 if jogador["posicao_secundaria"] == posicao else 0

    return count_primarias + count_secundarias

# Função para exibir os times


def exibir_times(times):
    order_of_positions = ['zagueiro', 'meia', 'atacante', None, 'Qualquer']

    # Mapeamento para formatar o nome das posições
    formatted_position_names = {'zagueiro': 'Zagueiros',
                                'meia': 'Meias', 'atacante': 'Atacantes', None: 'Nenhuma', 'Qualquer': 'Qualquer'}

    for i, time in enumerate(times, start=1):
        count_primary = count_primary_positions(time)
        count_secondary = count_secondary_positions(time)

        # Filtrar apenas as posições que têm valores não zerados
        non_zero_primary_positions = {posicao: count_primary.get(
            posicao, 0) for posicao in order_of_positions if count_primary.get(posicao, 0) != 0}
        non_zero_secondary_positions = {posicao: count_secondary.get(
            posicao, 0) for posicao in order_of_positions if count_secondary.get(posicao, 0) != 0}

        # Usar o mapeamento para formatar os nomes das posições
        positions_primary_output = ', '.join(
            [f"{formatted_position_names.get(posicao, posicao)}: {count}" for posicao, count in non_zero_primary_positions.items()])

        positions_secondary_output = ', '.join(
            [f"{formatted_position_names.get(posicao, posicao)}: {count}" for posicao, count in non_zero_secondary_positions.items()])

        print(f"Time {i} | Habilidade: {sum(j['habilidade'] for j in time)} | "
              f"Posições Primárias: {positions_primary_output} | "
              f"Posições Secundárias: {positions_secondary_output}")

        for jogador in time:
            habilidade = jogador['habilidade']
            adm = 'Sim' if jogador['adm'] else 'Não'
            posicao_primaria = jogador['posicao_primaria']
            # Verificar se a posição secundária está presente no mapeamento
            posicao_secundaria = formatted_position_names.get(
                jogador['posicao_secundaria'], 'Nenhuma')

            # print(f"  Jogador: {jogador['nome']} | Habilidade: {habilidade} | ADM: {adm} | POS-1: {formatted_position_names[posicao_primaria]} | POS-2: {formatted_position_names[posicao_secundaria]}")
            print(
                f"  Jogador: {jogador['nome']} | Habilidade: {habilidade} | POS-1: {formatted_position_names[posicao_primaria]} | POS-2: {posicao_secundaria}")

        print()


# Função auxiliar para contar a quantidade de jogadores em cada posição primária
def count_primary_positions(time):
    count = {}
    for jogador in time:
        posicao_primaria = jogador["posicao_primaria"]
        if posicao_primaria in count:
            count[posicao_primaria] += 1
        else:
            count[posicao_primaria] = 1
    return count

# Função auxiliar para contar a quantidade de jogadores em cada posição secundária


def count_secondary_positions(time):
    count = {}
    for jogador in time:
        posicao_secundaria = jogador.get("posicao_secundaria", None)
        if posicao_secundaria in count:
            count[posicao_secundaria] += 1
        else:
            count[posicao_secundaria] = 1
    return count


# Número de times
num_times = 5

# Número máximo de jogadores por time
max_jogadores_por_time = 5

# Criar os times
times = criar_times(jogadores, num_times)

# Exibir os times
# exibir_times(times)

# Trocar aleatoriamente os times
random.shuffle(times)

# Trocar aleatoriamente os jogadores dentro de cada time
for time in times:
    random.shuffle(time)

# Exibir os times após as trocas
print("\nTimes Sorteados:\n")
exibir_times(times)
