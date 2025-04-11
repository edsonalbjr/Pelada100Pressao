import unicodedata

# Lista de jogadores
jogadores = [
    {'nome': 'Albert', 'habilidade': 5, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'atacante', 'adm': True},
    {'nome': 'Alysson Pink', 'habilidade': 3, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Betinho', 'habilidade': 4, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'meia', 'adm': True},
    {'nome': 'Bruno Pessoa', 'habilidade': 4, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Claudino', 'habilidade': 5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Dato', 'habilidade': 4, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Diego Rocha', 'habilidade': 4.5, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Eduardo', 'habilidade': 4, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Eric', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'nenhum', 'adm': True},
    {'nome': 'Grimauro', 'habilidade': 2.5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Juninho', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Kiel', 'habilidade': 5, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Lucas H.', 'habilidade': 3, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Lucas S.', 'habilidade': 1, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Léo A.', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Manga', 'habilidade': 4, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Niclaudio', 'habilidade': 3, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Paulo Thiago', 'habilidade': 4, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Raphael B.', 'habilidade': 4, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Sérgio Falcão', 'habilidade': 2.5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Teixa', 'habilidade': 3, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Thiago Alemão', 'habilidade': 2, 'posicao_primaria': 'qualquer',
        'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Victor Chaves', 'habilidade': 3, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': True},
    {'nome': 'Vinicius', 'habilidade': 5, 'posicao_primaria': 'meia',
        'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Vitor S.', 'habilidade': 4, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Ícaro Feitosa', 'habilidade': 5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Cadu', 'habilidade': 5, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Xandinho', 'habilidade': 1, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Túlio', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro',
        'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Renan', 'habilidade': 5, 'posicao_primaria': 'atacante',
        'posicao_secundaria': 'meia', 'adm': False},
]

# Convertendo os dados da lista para o formato desejado e contando combinações de posições


def format_and_count(data):
    formatted_data = []
    position_combinations = {}

    for jogador in data:
        jogador_dict = {
            "nome": unicodedata.normalize('NFKD', str(jogador["nome"])),
            "habilidade": int(jogador["habilidade"]) if isinstance(jogador["habilidade"], int) else jogador["habilidade"],
            "posicao_primaria": unicodedata.normalize('NFKD', str(jogador["posicao_primaria"])),
            "posicao_secundaria": unicodedata.normalize('NFKD', str(jogador["posicao_secundaria"])),
            "adm": jogador["adm"]
        }

        formatted_data.append(jogador_dict)

        # Contando combinações de posições
        pos_comb = (jogador_dict["posicao_primaria"],
                    jogador_dict["posicao_secundaria"])
        position_combinations[pos_comb] = position_combinations.get(
            pos_comb, 0) + 1

    return formatted_data, position_combinations


# Formatação e contagem de combinações de posições
formatted_jogadores, position_combinations = format_and_count(jogadores)

# Define a ordem desejada das posições
ordered_positions = ['Zagueiro', 'Meia', 'Atacante', 'Qualquer', 'Nenhum']

print("\n*Contagem de posições hoje:*\n")

# Exibindo as contagens de combinações de posições na ordem desejada
primary_positions_count = {pos: 0 for pos in ordered_positions}
secondary_positions_count = {pos: 0 for pos in ordered_positions}

for comb, count in position_combinations.items():
    primary, secondary = comb
    primary_positions_count[primary.capitalize()] += count
    secondary_positions_count[secondary.capitalize()] += count

print("*Posições Primárias:*")
for pos, count in primary_positions_count.items():
    if count > 0:
        print(f"{count} {pos if count == 1 else pos +
              's' if pos not in ['Nenhum', 'Qualquer'] else pos}")

print("\n*Posições Secundárias:*")
for pos, count in secondary_positions_count.items():
    if count > 0:
        print(f"{count} {pos if count == 1 else pos +
              's' if pos not in ['Nenhum', 'Qualquer'] else pos}")
