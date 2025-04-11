import pandas as pd
import unicodedata

# Carregando o arquivo Excel
file_path = "bancodedados.xlsx"
df = pd.read_excel(file_path)

# Substituindo os valores NaN por None
df = df.where(pd.notna(df), None)

# Filtrando os dados com base na coluna "filiacao"
mensalista_data = df[df['filiacao'] == 'mensalista']
diarista_data = df[df['filiacao'] == 'diarista']

# Ordenando os jogadores por ordem alfabética
mensalista_data = mensalista_data.sort_values(by="jogador")
diarista_data = diarista_data.sort_values(by="jogador")

# Convertendo os dados filtrados para o formato desejado e contando combinações de posições
def format_and_count(data):
    formatted_data = []
    position_combinations = {}

    for _, jogador in data.iterrows():
        jogador_dict = {
            "nome": unicodedata.normalize('NFKD', str(jogador["jogador"])),
            "habilidade": int(jogador["habilidade"]) if pd.notna(jogador["habilidade"]) and jogador["habilidade"].is_integer() else jogador["habilidade"],
            "posicao_primaria": unicodedata.normalize('NFKD', str(jogador["posicao_primaria"])),
            "posicao_secundaria": unicodedata.normalize('NFKD', str(jogador["posicao_secundaria"])),
            "adm": True if unicodedata.normalize('NFKD', str(jogador["diretor"])) == 'sim' else False
        }

        formatted_data.append(jogador_dict)

        # Contando combinações de posições
        pos_comb = (jogador_dict["posicao_primaria"], jogador_dict["posicao_secundaria"])
        position_combinations[pos_comb] = position_combinations.get(pos_comb, 0) + 1

    return formatted_data, position_combinations

mensalista, mensalista_positions = format_and_count(mensalista_data)
diarista, diarista_positions = format_and_count(diarista_data)

# Define a ordem desejada das posições
ordered_positions = ['Zagueiro', 'Meia', 'Atacante', 'Qualquer', 'Nenhum']

print("\n*Contagem de combinações de posições:*\n")

# Exibindo as contagens de combinações de posições na ordem desejada
print("*Mensalistas:*")
for pos_comb in ordered_positions:
    for comb, count in mensalista_positions.items():
        if comb[0].capitalize() == pos_comb:
            print(f"{comb[0].capitalize()}, {comb[1].capitalize()}: {count}")

print("\n*Diaristas:*")
for pos_comb in ordered_positions:
    for comb, count in diarista_positions.items():
        if comb[0].capitalize() == pos_comb:
            print(f"{comb[0].capitalize()}, {comb[1].capitalize()}: {count}")


