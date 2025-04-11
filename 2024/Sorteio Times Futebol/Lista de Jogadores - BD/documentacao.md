# Documentação do Código

## Descrição
Este script Python lê um arquivo Excel contendo informações sobre jogadores de um time de futebol, realiza algumas operações de formatação nos dados, incluindo a correção da ordenação dos nomes com caracteres acentuados, e cria ou substitui um arquivo Python com os detalhes dos jogadores.

## Instruções de Uso
1. Certifique-se de ter o arquivo Excel `bancodedados.xlsx` no mesmo diretório do script.
2. Execute o script `app.py`.

## Código Python
<!-- ```python -->
import pandas as pd
import unicodedata
import locale

# Definindo a localização para considerar a ordenação alfabética correta para caracteres acentuados
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Carregando o arquivo Excel
file_path = "bancodedados.xlsx"
df = pd.read_excel(file_path)

# Substituindo os valores nan por None
df = df.where(pd.notna(df), None)

# Renomeando as colunas
df = df.rename(columns={"nome": "jogador", "adm": "diretor"})

# Filtrando os dados com base na coluna "filiacao"
mensalista_data = df[df['filiacao'] == 'mensalista']
diarista_data = df[df['filiacao'] == 'diarista']

# Ordenando os jogadores por ordem alfabética considerando a localização
mensalista_data = mensalista_data.sort_values(by="jogador", key=lambda x: x.astype(str).str.normalize('NFKD').str.encode('ASCII', 'ignore').str.decode())
diarista_data = diarista_data.sort_values(by="jogador", key=lambda x: x.astype(str).str.normalize('NFKD').str.encode('ASCII', 'ignore').str.decode())

# Convertendo os dados filtrados para o formato desejado
mensalista = [
    {"jogador": unicodedata.normalize('NFKD', str(jogador["jogador"])),
     "habilidade": int(jogador["habilidade"]) if jogador["habilidade"].is_integer() else jogador["habilidade"],
     "posicao_primaria": unicodedata.normalize('NFKD', str(jogador["posicao_primaria"])),
     "posicao_secundaria": unicodedata.normalize('NFKD', str(jogador["posicao_secundaria"])),
     "diretor": unicodedata.normalize('NFKD', str(jogador["diretor"]))}
    for _, jogador in mensalista_data.iterrows()
]

diarista = [
    {"jogador": unicodedata.normalize('NFKD', str(jogador["jogador"])),
     "habilidade": int(jogador["habilidade"]) if jogador["habilidade"].is_integer() else jogador["habilidade"],
     "posicao_primaria": unicodedata.normalize('NFKD', str(jogador["posicao_primaria"])),
     "posicao_secundaria": unicodedata.normalize('NFKD', str(jogador["posicao_secundaria"])),
     "diretor": unicodedata.normalize('NFKD', str(jogador["diretor"]))}
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

## Saída Esperada

> Arquivo lista_de_jogadores.py criado ou substituído com sucesso.

## Avisos
- Caso ocorram problemas de codificação ao escrever o arquivo, ajuste o parâmetro encoding para garantir a compatibilidade.
- Sempre faça backup dos dados antes de executar o script, pois ele substituirá o arquivo lista_de_jogadores.py existente.

## Autor
Edson Albuquerque

## Data
26/02/2024
