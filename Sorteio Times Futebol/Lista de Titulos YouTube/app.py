import datetime

# Obtém a data atual
data_atual = datetime.date.today()

# Diminui o dia em 1 para obter a data de ontem
data_ontem = data_atual - datetime.timedelta(days=1)

# Imprime o Titulo da Playlist
print()
print(f'Pelada 100 Pressão - {data_ontem.strftime('%d/%m/%Y')}\n')

# Imprime 15 titulos de videos para YouTube
for i in range(1, 16):
    # Formata o contador com zero à esquerda se for menor que 10
    contador_formatado = f"{i:02d}"

    print(f"Jogo {
          contador_formatado} - Pelada 100 Pressão - {data_ontem.strftime('%d/%m/%Y')}")

print()
print('Seja bem-vindo a Pelada 100 Pressão, a melhor organização de pelada do Brasil.\n')

print('Futebol, Futebol de campo, Futebol de salão, Campeonato, Times de futebol, Futebol brasileiro, Futebol internacional, Gols, Jogadas, Melhores momentos, Táticas de futebol, Treinamento de futebol, Jogadores famosos, Futebol de base, Futebol de rua, Curiosidades do futebol, Análises de jogos, Cobertura de competições, Entrevistas com jogadores e treinadores, Futebol de base, Documentários de futebol, Futebol de freestyle, Desafios de futebol, Jogos clássicos, Futebol de videogame, Habilidades de futebol, Lances incríveis, Treinadores de futebol, História do futebol, Futebol de praia, Futebol de seleções, Copa do Mundo, UEFA Champions League, Campeonato Brasileiro.\n')

print('Bom dia, os Vídeos já estão no YouTube ▶️:  ')