import pandas as pd

# Carregar as planilhas
planilha1 = pd.read_excel('1.xlsx')
planilha2 = pd.read_excel('2.xlsx')

# Concatenar as duas planilhas
consolidado = pd.concat([planilha1, planilha2])

# Agrupar os dados pelo jogador e somar os gols
consolidado = consolidado.groupby('jogador', as_index=False)['gols', 'assistências'].sum()

# Salvar o arquivo consolidado
consolidado.to_excel('dados-consolidados.xlsx', index=False)

print("Dados consolidados gerados com sucesso!")
