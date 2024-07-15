from collections import defaultdict

# Ler os nomes do arquivo nomes.txt com codificação utf-8
with open('nomes.txt', 'r', encoding='utf-8') as file:
    nomes = file.readlines()

# Dicionário para armazenar os pontos de cada nome
pontuacao = defaultdict(int)

# Contagem dos pontos
for nome in nomes:
    nome = nome.strip()  # Remover espaços em branco e quebras de linha
    nome_ponto = nome.split(' ')[0]
    if "✅" in nome:
        pontuacao[nome_ponto] += 2
    elif "❌" in nome:
        pontuacao[nome_ponto] += 0
    else:
        pontuacao[nome_ponto] += 1

# Gerar o ranking
ranking = sorted(pontuacao.items(), key=lambda x: x[1], reverse=True)

# Imprimir o ranking
print("Ranking de frequencia dos diaristas:")
for posicao, (nome, pontos) in enumerate(ranking, start=1):
    print(f"{posicao}. {nome} - {pontos} pontos")
