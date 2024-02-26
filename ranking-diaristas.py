from collections import defaultdict

# Lista de nomes com os respectivos status
nomes = [

    "Alysson Pink ❌", "Alysson Pink ✅", "Alysson Pink ✅", "Alysson Pink ✅", "Alysson Pink ✅", "Alysson Pink ✅", "Alysson Pink ✅", "Alysson Pink ✅", "Alysson Pink ✅", "Alysson Pink ✅", "Alysson Pink ✅"
    "Arthur ✅",
    "Balbino ❌", "Balbino ✅", "Balbino ✅",
    "Bidu ✅", "Bidu ✅", "Bidu ✅",
    "Breno ❌",
    "Christopher ✅", "Christopher ❌", "Christopher ❌",
    "Elvinho ❌", "Elvinho ❌",
    "Felipe Melo ❌", "Felipe Melo ✅",
    "Gabriel ✅", "Gabriel ✅",
    "Grimauro ❌", "Grimauro ❌", "Grimauro ❌", "Grimauro ✅", "Grimauro ✅", "Grimauro ✅", "Grimauro ✅",
    'Henrique Souza ❌',
    "Ícaro ❌", "Ícaro ✅", "Ícaro ✅", "Ícaro ✅", "Ícaro ❌",
    "Jackson ❌", "Jackson ✅", "Jackson ❌", "Jackson ❌", "Jackson ✅", "Jackson ✅", "Jackson ✅",
    "Jefferson ❌", "Jefferson ✅", "Jefferson ✅", "Jefferson ✅",
    "Jorge ❌", "Jorge ❌",
    "Juninho ❌", "Juninho ❌", "Juninho ✅", "Juninho ✅", "Juninho ✅", "Juninho ✅", "Juninho ✅", "Juninho ✅", "Juninho ✅", "Juninho ✅",
    "Lazaro ❌", "Lazaro ✅",
    "Leo ❌", "Leo ✅", "Leo ✅", "Leo ❌",
    "Lucas Paranhos ❌", 'Lucas Paranhos ❌',
    "Nagibio ❌",
    "Nagibio ✅", "Nagibio ✅",
    "Neto ❌", "Neto ✅", "Neto ✅", "Neto ✅", "Neto ✅", "Neto ✅",
    "Pedro ❌", "Pedro ❌", "Pedro ❌",
    "Pou ✅", "Pou ✅",
    "Reynods ✅",
    "Ronaldinho ✅", "Ronaldinho ✅", "Ronaldinho ✅",
    "Sérgio ❌", "Sérgio ❌", "Sérgio ✅", "Sérgio ✅", "Sérgio ✅", "Sérgio ✅", "Sérgio ✅", "Sérgio ✅", "Sérgio ✅",
    "Teffinho ✅", "Teffinho ✅",
    "Teteca ❌", "Teteca ❌",
    'Tulio B. ✅',
    'Winnicius C. ❌', "Winnicius C. ✅", "Winnicius C. ✅", "Winnicius C. ✅", "Winnicius C. ✅", "Winnicius C. ✅", "Winnicius C. ✅", "Winnicius C. ✅", "Winnicius C. ✅",
    'Xand ❌', 'Xand ❌', 'Xand ❌', 'Xand ✅'
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
