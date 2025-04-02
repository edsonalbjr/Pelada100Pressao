import random

jogadores_sorteio = mensalistas = [
    {'nome': 'Betinho', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Bidu', 'habilidade': 3, 'posicao_primaria': 'meia', 'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Bruno Pessoa', 'habilidade': 4.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': True},
    {'nome': 'Dato', 'habilidade': 3.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Diego Rocha', 'habilidade': 4.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Eduardo', 'habilidade': 4, 'posicao_primaria': 'meia', 'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Grimauro', 'habilidade': 2, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Jackson', 'habilidade': 4, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'João Vitor', 'habilidade': 4.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Juninho', 'habilidade': 3, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Kiel', 'habilidade': 4.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': True},
    {'nome': 'Léo A.', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Lucas H.', 'habilidade': 3, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Lucas S.', 'habilidade': 1, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Manga', 'habilidade': 4.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Marcos S.', 'habilidade': 3.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Paulo Thiago', 'habilidade': 3.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Rafa Ribeiro', 'habilidade': 3, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Raphael B.', 'habilidade': 3.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Sérgio Falcão', 'habilidade': 2.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Teixa', 'habilidade': 2.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Thayan', 'habilidade': 3.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Thiago Alemão', 'habilidade': 2, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Túlio', 'habilidade': 3, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Victor Chaves', 'habilidade': 3, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Xandinho', 'habilidade': 1, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Flavio Ureia', 'habilidade': 3.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Renan', 'habilidade': 3.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Thiago Sultanum', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Elder', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'atacante', 'adm': False},
]


print(f'\nJogadores Sorteados: {len(jogadores_sorteio)}')


# Função para criar times com base nas habilidade e posições dos jogadores_sorteio
def criar_times(jogadores_sorteio, num_times):
    # Fazer uma cópia aleatória da lista de jogadores_sorteio
    jogadores_copia = random.sample(jogadores_sorteio, len(jogadores_sorteio))

    # Separar jogadores_sorteio com 'adm': True e 'adm': False
    jogadores_adm_true = [j for j in jogadores_copia if j['adm']]
    jogadores_adm_false = [j for j in jogadores_copia if not j['adm']]

    # Ordenar ambos os grupos por habilidade de forma decrescente
    jogadores_adm_true = sorted(
        jogadores_adm_true, key=lambda x: x["habilidade"], reverse=True)
    jogadores_adm_false = sorted(
        jogadores_adm_false, key=lambda x: x["habilidade"], reverse=True)

    # Inicializa os times como listas vazias
    times = [[] for _ in range(num_times)]

    # Distribui jogadores_sorteio com 'adm': True primeiro
    for jogador in jogadores_adm_true:
        # Encontra o time com menor número de jogadores_sorteio e posições equilibradas
        menor_time = min(times, key=lambda t: (
            sum(j["habilidade"] for j in t), count_positions(t, jogador)))

        # Adiciona o jogador ao time
        menor_time.append(jogador)

        # Remove o jogador da lista geral apenas se não for "qualquer"
        if jogador["posicao_primaria"] != "qualquer":
            jogadores_sorteio.remove(jogador)

        # Verifica se todos os jogadores_sorteio foram distribuídos
        if not jogadores_sorteio:
            break

    # Distribui os jogadores_sorteio com 'adm': False
    for jogador in jogadores_adm_false:
        # Se a posição primária for "qualquer", distribui o jogador para o time com menor habilidade
        if jogador["posicao_primaria"] == "qualquer":
            menor_time = min(times, key=lambda t: sum(
                j["habilidade"] for j in t))
            menor_time.append(jogador)
            if jogador["posicao_primaria"] != "qualquer":
                jogadores_sorteio.remove(jogador)
            if not jogadores_sorteio:
                break
        else:
            # Encontra o time com menor número de jogadores_sorteio e posições equilibradas
            menor_time = min(times, key=lambda t: (
                sum(j["habilidade"] for j in t), count_positions(t, jogador)))

            # Adiciona o jogador ao time
            menor_time.append(jogador)

            # Remove o jogador da lista geral apenas se não for "qualquer"
            if jogador["posicao_primaria"] != "qualquer":
                jogadores_sorteio.remove(jogador)

            # Verifica se todos os jogadores_sorteio foram distribuídos
            if not jogadores_sorteio:
                break

    return times


# Função auxiliar para contar a quantidade de jogadores_sorteio em cada posição
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
            [f"{count} {formatted_position_names.get(posicao, posicao).capitalize()[0:3]}" for posicao, count in non_zero_primary_positions.items()])

        # Usar o mapeamento para formatar os nomes das posições secundárias
        positions_secondary_output = ', '.join(
            [f"{count} {formatted_position_names.get(posicao, posicao).capitalize()[0:3]}" for posicao, count in non_zero_secondary_positions.items()])

        # Print informações dos times completo
        print(f'*--------------- Time {i} ---------------*')
        habilidade_total = sum(j['habilidade'] for j in time)
        # Formatar a habilidade total para exibir como inteiro se for o caso
        formatted_habilidade_total = int(
            habilidade_total) if habilidade_total.is_integer() else habilidade_total
        print(f"*Time {i} | {formatted_habilidade_total} Estrelas*\n" f"1° Posição: {
            positions_primary_output}\n" f"2° Posição: {positions_secondary_output}\n")
        # Print informações dos times completo

        habilidade_time = sum(j['habilidade'] for j in time)

        # Verifica se a habilidade total do time é um número inteiro
        if habilidade_time % 1 == 0:
            habilidade_time = int(habilidade_time)

        for j, jogador in enumerate(time, start=1):
            habilidade = jogador['habilidade']
            adm = 'Sim' if jogador['adm'] else 'Não'
            posicao_primaria = jogador['posicao_primaria']
            posicao_secundaria = formatted_position_names.get(
                jogador['posicao_secundaria'], 'Nenhum')

            # Usar o mapeamento para formatar os nomes das posições dos jogadores_sorteio
            posicao_primaria_formatada = formatted_position_names.get(
                posicao_primaria, posicao_primaria).capitalize()[0:3]
            posicao_secundaria_formatada = formatted_position_names.get(
                posicao_secundaria, posicao_secundaria).capitalize()[0:3]

            # Print informações dos jogadores_sorteio completo
            if posicao_secundaria_formatada != "Nen":
                print(f"*{jogador['nome']}* | {int(habilidade) if habilidade % 1 == 0 else habilidade} Estrelas | {
                      posicao_primaria_formatada}/{posicao_secundaria_formatada}")
            else:
                print(f"*{jogador['nome']}* | {int(habilidade) if habilidade %
                      1 == 0 else habilidade} Estrelas | {posicao_primaria_formatada}")
            # Print informações dos jogadores_sorteio completo

        print()


# Função auxiliar para contar a quantidade de jogadores_sorteio em cada posição primária
def count_primary_positions(time):
    count = {}
    for jogador in time:
        posicao_primaria = jogador["posicao_primaria"]
        if posicao_primaria in count:
            count[posicao_primaria] += 1
        else:
            count[posicao_primaria] = 1
    return count


# Função auxiliar para contar a quantidade de jogadores_sorteio em cada posição secundária
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

# Número máximo de jogadores_sorteio por time
max_jogadores_por_time = 6

# Criar os times
times = criar_times(jogadores_sorteio, num_times)

# Trocar aleatoriamente os times
random.shuffle(times)

# Ordenar os jogadores_sorteio dentro de cada time por habilidade (do maior para o menor)
for time in times:
    time.sort(key=lambda jogador: jogador['habilidade'], reverse=True)

# Exibir os times após as trocas
print("\n*Times Sorteados*\n")
exibir_times(times)
