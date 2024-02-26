import pandas as pd
import json

# Carregando o arquivo Excel
file_path = "bancodedados.xlsx"
df = pd.read_excel(file_path)

# Verificando se todas as colunas necessárias estão presentes no DataFrame
colunas_necessarias = ["nome", "habilidade", "adm",
                       "posicao_primaria", "posicao_secundaria", "filiacao"]
if not set(colunas_necessarias).issubset(df.columns):
    raise ValueError("Colunas necessárias não encontradas no DataFrame")

# Substituindo os valores nan por None
df = df.where(pd.notna(df), None)

# Filtrando os dados com base na coluna "filiacao"
mensalista_data = df[df['filiacao'] == 'mensalista']
diarista_data = df[df['filiacao'] == 'diarista']

# Convertendo os dados filtrados para o formato desejado
mensalista = [
    {"nome": jogador["nome"], "habilidade": jogador["habilidade"], "posicao_primaria": jogador["posicao_primaria"],
     "posicao_secundaria": jogador["posicao_secundaria"],
     "adm": jogador["adm"]}
    for _, jogador in mensalista_data.iterrows()
]

diarista = [
    {"nome": jogador["nome"], "habilidade": jogador["habilidade"], "posicao_primaria": jogador["posicao_primaria"],
     "posicao_secundaria": jogador["posicao_secundaria"],
     "adm": jogador["adm"]}
    for _, jogador in diarista_data.iterrows()
]

# Exibindo os resultados
print("\nmensalistas = [")
for jogador in mensalista:
    print("    " + str(jogador) + ",")
print("]")

print("\ndiaristas = [")
for jogador in diarista:
    print("    " + str(jogador) + ",")
print("]")
