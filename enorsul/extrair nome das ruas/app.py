import pandas as pd


def extrair_nomes_ruas(arquivo_excel):
    # Carregando o arquivo Excel
    df = pd.read_excel(arquivo_excel)

    # Extraindo apenas os nomes das ruas
    nomes_ruas = df['rua'].apply(lambda x: x.split(',')[0])

    # Removendo duplicatas
    nomes_ruas_sem_repeticao = nomes_ruas.drop_duplicates()

    # Convertendo para uma lista de strings
    lista_nomes_ruas = nomes_ruas_sem_repeticao.tolist()

    return lista_nomes_ruas


if __name__ == "__main__":
    # Substitua 'seuarquivo.xlsx' pelo caminho do seu arquivo Excel
    nomes_ruas = extrair_nomes_ruas('rua.xlsx')

    # Imprimindo os nomes das ruas
    for rua in nomes_ruas:
        print(rua)
