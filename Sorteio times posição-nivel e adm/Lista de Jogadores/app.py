import pandas as pd
import unicodedata

# Carregando o arquivo Excel
file_path = "bancodedados.xlsx"
df = pd.read_excel(file_path)

# Substituindo os valores nan por None
df = df.where(pd.notna(df), None)

# Renomeando as colunas
# df = df.rename(columns={"nome": "jogador", "adm": "diretor"})

# Filtrando os dados com base na coluna "filiacao"
mensalista_data = df[df['filiacao'] == 'mensalista']
diarista_data = df[df['filiacao'] == 'diarista']

# Convertendo os dados filtrados para o formato desejado
mensalista = [
    {"jogador": unicodedata.normalize('NFKD', str(jogador["jogador"])),
     "habilidade": int(jogador["habilidade"]) if jogador["habilidade"].is_integer() else jogador["habilidade"],
     "posicao_primaria": unicodedata.normalize('NFKD', str(jogador["posicao_primaria"])),
     "posicao_secundaria": unicodedata.normalize('NFKD', str(jogador["posicao_secundaria"])),
     "adm": unicodedata.normalize('NFKD', str(jogador["diretor"]))}
    for _, jogador in mensalista_data.iterrows()
]

diarista = [
    {"jogador": unicodedata.normalize('NFKD', str(jogador["jogador"])),
     "habilidade": int(jogador["habilidade"]) if jogador["habilidade"].is_integer() else jogador["habilidade"],
     "posicao_primaria": unicodedata.normalize('NFKD', str(jogador["posicao_primaria"])),
     "posicao_secundaria": unicodedata.normalize('NFKD', str(jogador["posicao_secundaria"])),
     "adm": unicodedata.normalize('NFKD', str(jogador["diretor"]))}
    for _, jogador in diarista_data.iterrows()
]

# Criando ou substituindo o arquivo lista_de_jogadores.py
with open("lista_de_jogadores.py", "w", encoding="utf-8") as file:
    file.write("mensalistas = [\n")
    for jogador in mensalista:
        file.write("    " + str(jogador) + ",\n")
    file.write("]\n\n")

    file.write("diaristas = [\n")
    for jogador in diarista:
        file.write("    " + str(jogador) + ",\n")
    file.write("]\n")


print("\n> Arquivo lista_de_jogadores.py criado ou substituído com sucesso.\n")
