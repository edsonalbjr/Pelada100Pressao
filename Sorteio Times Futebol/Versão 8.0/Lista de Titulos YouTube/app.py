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

print('*Os Vídeos já estão no YouTube ▶️:* #LINK DA PLAYLIST#\n')

# print('*Vou postar apenas 3 melhores momentos por semana. Então, caso tenham algum lance que queiram ver no feed do Instagram e YouTube, enviem aqui:*\n')

# print('https://forms.gle/ENzkSzjmt4MyoWrdA\n')

# print('*1. Escolha o tipo do lance;*')
# print('*2. Informe em qual jogo aconteceu;*')
# print('*3. Indique o minuto e segundo do início do lance;*')
# print('*4. Indique o minuto e segundo do fim do lance.*')
