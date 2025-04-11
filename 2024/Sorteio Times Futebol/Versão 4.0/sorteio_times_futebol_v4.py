import random

jogadores = mensalistas = [
    {'nome': 'Albert', 'habilidade': 5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': True},
    {'nome': 'Alysson Pink', 'habilidade': 3, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Betinho', 'habilidade': 4, 'posicao_primaria': 'meia', 'posicao_secundaria': 'zagueiro', 'adm': True},
    {'nome': 'Bidu', 'habilidade': 4, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Bruno Pessoa', 'habilidade': 4, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Eduardo', 'habilidade': 4, 'posicao_primaria': 'meia', 'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Grimauro', 'habilidade': 2.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Juninho', 'habilidade': 3, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Kiel', 'habilidade': 4.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Lucas H.', 'habilidade': 3, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Léo A.', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Manga', 'habilidade': 4.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Niclaudio', 'habilidade': 3, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Paulo Thiago', 'habilidade': 4, 'posicao_primaria': 'meia', 'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Raphael B.', 'habilidade': 4, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Sérgio Falcão', 'habilidade': 2.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Teixa', 'habilidade': 3, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Thiago Alemão', 'habilidade': 2, 'posicao_primaria': 'qualquer', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Victor Chaves', 'habilidade': 3, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': True},
    {'nome': 'Vinicius', 'habilidade': 5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Vitor S.', 'habilidade': 4, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    

    {'nome': 'Neto', 'habilidade': 3.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
{'nome': 'Túlio', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'meia', 'adm': False},
{'nome': 'Xandinho', 'habilidade': 1, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'zagueiro', 'adm': False},
{'nome': 'Renan', 'habilidade': 5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
{'nome': 'Flavio U.', 'habilidade': 4.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
{'nome': 'Arthur', 'habilidade': 3, 'posicao_primaria': 'qualquer', 'posicao_secundaria': 'nenhum', 'adm': False},
{'nome': 'Lucas', 'habilidade': 5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
{'nome': 'Gabriel', 'habilidade': 2, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
{'nome': 'Serginho', 'habilidade': 3, 'posicao_primaria': 'qualquer', 'posicao_secundaria': 'nenhum', 'adm': False},

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
            sum(j["habilidade"] for j in t), contar_posicoes(t, jogador)))

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
                sum(j["habilidade"] for j in t), contar_posicoes(t, jogador)))

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
def contar_posicoes(time, jogador, posicao=None):
    countar_primarias = sum(
        1 for j in time if j["posicao_primaria"] == jogador["posicao_primaria"])
    countar_secundarias = sum(
        1 for j in time if j["posicao_secundaria"] == jogador["posicao_secundaria"])

    if posicao:
        countar_primarias += 1 if jogador["posicao_primaria"] == posicao else 0
        countar_secundarias += 1 if jogador["posicao_secundaria"] == posicao else 0

    return countar_primarias + countar_secundarias


# Função para exibir os times
def exibir_times(times):
    ordem_de_posicoes = ['zagueiro', 'meia', 'atacante', None, 'qualquer']

    # Mapeamento para formatar o nome das posições
    nomes_de_posicao_formatados = {'zagueiro': 'Zagueiro',
                                'meia': 'Meia', 'atacante': 'Atacante', None: 'Nenhum', 'qualquer': 'Qualquer'}

    for i, time in enumerate(times, start=1):
        contagem_primaria = contagem_posicoes_primarias(time)
        contagem_secundaria = contagem_posicoes_secundarias(time)

        # Filtrar apenas as posições que têm valores não zerados
        non_zero_primary_positions = {posicao: contagem_primaria.get(
            posicao, 0) for posicao in ordem_de_posicoes if contagem_primaria.get(posicao, 0) != 0}
        non_zero_secondary_positions = {posicao: contagem_secundaria.get(
            posicao, 0) for posicao in ordem_de_posicoes if contagem_secundaria.get(posicao, 0) != 0}

        # Usar o mapeamento para formatar os nomes das posições primárias
        posicoes_primario_saida = ', '.join(
            [f"{count} {nomes_de_posicao_formatados.get(posicao, posicao).capitalize()[0:3]}" for posicao, count in non_zero_primary_positions.items()])

        # Usar o mapeamento para formatar os nomes das posições secundárias
        posicoes_secundario_saida = ', '.join(
            [f"{count} {nomes_de_posicao_formatados.get(posicao, posicao).capitalize()[0:3]}" for posicao, count in non_zero_secondary_positions.items()])

        # Print informações dos times completo
        print(f'*--------------- Time {i} ---------------*')
        habilidade_total = sum(j['habilidade'] for j in time)
        # Formatar a habilidade total para exibir como inteiro se for o caso
        formatado_habilidade_total = int(
            habilidade_total) if habilidade_total.is_integer() else habilidade_total
        print(f"*Time {i} | {formatado_habilidade_total} Estrelas*\n" f"1° Posição: {
            posicoes_primario_saida}\n" f"2° Posição: {posicoes_secundario_saida}\n")
        # Print informações dos times completo

        habilidade_time = sum(j['habilidade'] for j in time)

        # Verifica se a habilidade total do time é um número inteiro
        if habilidade_time % 1 == 0:
            habilidade_time = int(habilidade_time)

        for j, jogador in enumerate(time, start=1):
            habilidade = jogador['habilidade']
            adm = 'Sim' if jogador['adm'] else 'Não'
            posicao_primaria = jogador['posicao_primaria']
            posicao_secundaria = nomes_de_posicao_formatados.get(
                jogador['posicao_secundaria'], 'Nenhum')

            # Usar o mapeamento para formatar os nomes das posições dos jogadores
            posicao_primaria_formatada = nomes_de_posicao_formatados.get(
                posicao_primaria, posicao_primaria).capitalize()[0:3]
            posicao_secundaria_formatada = nomes_de_posicao_formatados.get(
                posicao_secundaria, posicao_secundaria).capitalize()[0:3]

            # Print informações dos jogadores completo
            if posicao_secundaria_formatada != "Nen":
                print(f"*{jogador['nome']}* | {int(habilidade) if habilidade % 1 == 0 else habilidade} Estrelas | {
                      posicao_primaria_formatada}/{posicao_secundaria_formatada}")
            else:
                print(f"*{jogador['nome']}* | {int(habilidade) if habilidade %
                      1 == 0 else habilidade} Estrelas | {posicao_primaria_formatada}")
            # Print informações dos jogadores completo

        print()


# Função auxiliar para contar a quantidade de jogadores em cada posição primária
def contagem_posicoes_primarias(time):
    count = {}
    for jogador in time:
        posicao_primaria = jogador["posicao_primaria"]
        if posicao_primaria in count:
            count[posicao_primaria] += 1
        else:
            count[posicao_primaria] = 1
    return count


# Função auxiliar para contar a quantidade de jogadores em cada posição secundária
def contagem_posicoes_secundarias(time):
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

# Trocar aleatoriamente os times
random.shuffle(times)

# Ordenar os jogadores dentro de cada time por habilidade (do maior para o menor)
for time in times:
    time.sort(key=lambda jogador: jogador['habilidade'], reverse=True)

# Exibir os times após as trocas
print("\n*Times Sorteados*\n")
exibir_times(times)
