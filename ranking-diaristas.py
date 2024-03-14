from collections import defaultdict

# Lista de nomes com os respectivos status
nomes = [
    'Ícaro ✅',
    'Xand ✅',
    'Ronaldinho ✅',
    'Chris ✅',
    'Juninho ❌',
    'Neto ❌',
    'Sérgio ❌',
    'Leo A. ❌',
    'Cadu ❌',
    'Túlio',
    'Claudino ❌',
    'Grima ❌',
    'Jefferson ❌',
    'João ❌',
    'Gabriel ❌',
    'Xand ❌',
    'Renan ✅',
    'Ronaldinho ✅',
    'Túlio ✅',
    'Léo ✅',
    'Cadu ✅',
    'Sérgio ✅',
    'Juninho ✅',
    'Ícaro ✅',
    'Grima ❌',
    'Claudino ❌',
    'Jefferson ✅'
]

# Dicionário para armazenar os pontos de cada nome
pontuacao = defaultdict(int)

# Contagem dos pontos
for nome in nomes:
    nome_ponto = nome.split(' ')[0]
    if "✅" in nome:
        pontuacao[nome_ponto] += 2
    elif "❌" in nome:
        pontuacao[nome_ponto] += 1

# Gerar o ranking
ranking = sorted(pontuacao.items(), key=lambda x: x[1], reverse=True)

# Imprimir o ranking
print("Ranking:")
for posicao, (nome, pontos) in enumerate(ranking, start=1):
    print(f"{nome} - {pontos} pontos")
