import pandas as pd
import unicodedata

# Carregando o arquivo Excel
file_path = "bancodedados.xlsx"
df = pd.read_excel(file_path)

# Substituindo os valores nan por None
df = df.where(pd.notna(df), None)

# Convertendo os dados filtrados para o formato desejado
jogadores = [
    {
        "id": jogador["id"],
        "nome": unicodedata.normalize('NFKD', str(jogador["jogador"])),
        "habilidade": int(jogador["habilidade"]) if pd.notna(jogador["habilidade"]) and jogador["habilidade"].is_integer() else jogador["habilidade"],
        "posicao_primaria": unicodedata.normalize('NFKD', str(jogador["posicao_primaria"])),
        "posicao_secundaria": unicodedata.normalize('NFKD', str(jogador["posicao_secundaria"])),
        "filiacao": unicodedata.normalize('NFKD', str(jogador["filiacao"])),
        "adm": True if unicodedata.normalize('NFKD', str(jogador["diretor"])) == 'sim' else False
    }
    for _, jogador in df.iterrows()
]

# Criando ou substituindo o arquivo lista_de_jogadores.py
with open("lista_de_jogadores.py", "w", encoding="utf-8") as file:
    file.write("jogadores = [\n")
    for jogador in jogadores:
        file.write("    " + str(jogador) + ",\n")
    file.write("]\n")

print("\n> Arquivo lista_de_jogadores.py criado ou substituído com sucesso.\n")
