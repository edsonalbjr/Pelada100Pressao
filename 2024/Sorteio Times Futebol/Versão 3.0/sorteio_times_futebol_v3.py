import random

jogadores = [
    {'nome': 'Albert', 'habilidade': 5, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'atacante', 'adm': True},
    {'nome': 'Alysson Pink', 'habilidade': 3, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Betinho', 'habilidade': 4, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'meia', 'adm': True},
    {'nome': 'Bidu', 'habilidade': 4, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Bruno Pessoa', 'habilidade': 4, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Dato', 'habilidade': 4, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Eduardo', 'habilidade': 4, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Eric ', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'nenhum', 'adm': True},
    {'nome': 'Kiel', 'habilidade': 5, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Lucas Henrique', 'habilidade': 3, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Lucas Silveira', 'habilidade': 1, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Manga ', 'habilidade': 4, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Paulo Thiago', 'habilidade': 4, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Raphael Borges', 'habilidade': 4, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Teixa', 'habilidade': 3, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Thiago Alemão', 'habilidade': 2, 'posicao_primaria': 'qualquer',
        'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Victor Assis', 'habilidade': 3, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Renan', 'habilidade': 5, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Ronaldinho', 'habilidade': 3.5, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Túlio', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Leo Albuquerque', 'habilidade': 3.5,
        'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Cadu', 'habilidade': 5, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Sérgio', 'habilidade': 2.5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Juninho', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Ícaro Feitosa', 'habilidade': 5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'meia', 'adm': False},
]

print(f'\nJogadores Sorteados: {len(jogadores)}')

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

        # Remove o jogador da lista geral apenas se não for "qualquer"
        if jogador["posicao_primaria"] != "qualquer":
            jogadores.remove(jogador)

        # Verifica se todos os jogadores foram distribuídos
        if not jogadores:
            break

    # Distribui os jogadores com 'adm': False
    for jogador in jogadores_adm_false:
        # Se a posição primária for "qualquer", distribui o jogador para o time com menor habilidade
        if jogador["posicao_primaria"] == "qualquer":
            menor_time = min(times, key=lambda t: sum(
                j["habilidade"] for j in t))
            menor_time.append(jogador)
            if jogador["posicao_primaria"] != "qualquer":
                jogadores.remove(jogador)
            if not jogadores:
                break
        else:
            # Encontra o time com menor número de jogadores e posições equilibradas
            menor_time = min(times, key=lambda t: (
                sum(j["habilidade"] for j in t), count_positions(t, jogador)))

            # Adiciona o jogador ao time
            menor_time.append(jogador)

            # Remove o jogador da lista geral apenas se não for "qualquer"
            if jogador["posicao_primaria"] != "qualquer":
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


# Função para exibir os times
def exibir_times(times):
    order_of_positions = ['zagueiro', 'meia', 'atacante', None, 'qualquer']

    # Mapeamento para formatar o nome das posições
    formatted_position_names = {'zagueiro': 'Zagueiro',
                                'meia': 'Meia', 'atacante': 'Atacante', None: 'Nenhum', 'qualquer': 'Qualquer'}

    for i, time in enumerate(times, start=1):
        count_primary = count_primary_positions(time)
        count_secondary = count_secondary_positions(time)

        # Filtrar apenas as posições que têm valores não zerados
        non_zero_primary_positions = {posicao: count_primary.get(
            posicao, 0) for posicao in order_of_positions if count_primary.get(posicao, 0) != 0}
        non_zero_secondary_positions = {posicao: count_secondary.get(
            posicao, 0) for posicao in order_of_positions if count_secondary.get(posicao, 0) != 0}

        # Usar o mapeamento para formatar os nomes das posições primárias
        positions_primary_output = ', '.join(
            [f"{formatted_position_names.get(posicao, posicao).capitalize() + ('s' if count > 1 and posicao not in ['qualquer', 'nenhum'] else '')}: {count}" for posicao, count in non_zero_primary_positions.items()])

        # Usar o mapeamento para formatar os nomes das posições secundárias
        positions_secondary_output = ', '.join(
            [f"{formatted_position_names.get(posicao, posicao).capitalize() + ('s' if count > 1 and posicao not in ['qualquer', 'nenhum'] else '')}: {count}" for posicao, count in non_zero_secondary_positions.items()])

        # Print Completo
        print(f"Time {i} | Habilidade: {sum(j['habilidade'] for j in time)}\n"
              f"Posições Primárias: {positions_primary_output}\n"
              f"Posições Secundárias: {positions_secondary_output}\n")
        # Print Completo

        habilidade_time = sum(j['habilidade'] for j in time)

        # Verifica se a habilidade total do time é um número inteiro
        if habilidade_time % 1 == 0:
            habilidade_time = int(habilidade_time)

        # Print informações do time resumido
        # print(f"Time {i} | Habilidade: {habilidade_time}\n"
        #       f"1° POS.: {positions_primary_output}\n"
        #       f"2° POS.: {positions_secondary_output}\n")
        # Print informações do time resumido

        # Print informações do time mais resumido
        # print(f"Time {i}")
        # Print informações do time mais resumido

        for j, jogador in enumerate(time, start=1):
            habilidade = jogador['habilidade']
            adm = 'Sim' if jogador['adm'] else 'Não'
            posicao_primaria = jogador['posicao_primaria']
            posicao_secundaria = formatted_position_names.get(
                jogador['posicao_secundaria'], 'Nenhum')

            # Usar o mapeamento para formatar os nomes das posições dos jogadores
            posicao_primaria_formatada = formatted_position_names.get(
                posicao_primaria, posicao_primaria).capitalize()
            posicao_secundaria_formatada = formatted_position_names.get(
                posicao_secundaria, posicao_secundaria).capitalize()

            # Print informações dos jogadores completo
            print(f"  Jogador {j}: {jogador['nome']} | Habilidade: {int(habilidade) if habilidade % 1 ==
                  0 else habilidade} | POS-1: {posicao_primaria_formatada} | POS-2: {posicao_secundaria_formatada}")
            # Print informações dos jogadores completo

            # Print informações dos jogadores resumido
            # print(f"{jogador['nome']}, {int(habilidade) if habilidade % 1 == 0 else habilidade}, {posicao_primaria_formatada}, {posicao_secundaria_formatada}")
            # Print informações dos jogadores resumido
            # Print informações dos jogadores mais resumido
            # print(f"{jogador['nome']}")
            # Print informações dos jogadores mais resumido

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
