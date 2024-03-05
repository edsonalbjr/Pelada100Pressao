import datetime

# Obtém a data atual
data_atual = datetime.date.today()

# Diminui o dia em 1 para obter a data de ontem
data_ontem = data_atual - datetime.timedelta(days=1)

# Imprime o Titulo da Playlist
print(f'Pelada 100 Pressão - {data_ontem.strftime('%d/%m/%Y')}\n')

# Imprime 15 titulos de videos para YouTube
for i in range(1, 16):
    # Formata o contador com zero à esquerda se for menor que 10
    contador_formatado = f"{i:02d}"

    print(f"Jogo {
          contador_formatado} - Pelada 100 Pressão - {data_ontem.strftime('%d/%m/%Y')}")
