import random
import sys
import os

# Adicionar o diretório do arquivo lista_de_jogadores.py ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Lista de Jogadores - BD'))
from lista_de_jogadores import mensalistas, diaristas

# Juntar todos os jogadores em uma única lista
todos_jogadores = mensalistas + diaristas

# Filtrar apenas jogadores com posições específicas
posicoes_validas = ['atacante', 'meia', 'zagueiro']
jogadores_filtrados = [
    jogador for jogador in todos_jogadores
    if jogador['posicao_primaria'] in posicoes_validas and
    (jogador['posicao_secundaria'] in posicoes_validas or jogador['posicao_secundaria'] == 'nenhum')
]

# Função para gerar um sorteio
def gerar_sorteio(numero_sorteio):
    # Embaralhar os jogadores filtrados
    jogadores_embaralhados = random.sample(jogadores_filtrados, len(jogadores_filtrados))
    # Pegar os 30 primeiros jogadores
    sorteio = jogadores_embaralhados[:30]
    return sorteio

# Gerar 5 sorteios diferentes
sorteios = {}
for i in range(1, 6):
    sorteios[f'sorteio_{i}'] = gerar_sorteio(i)

# Salvar os sorteios em um arquivo
with open('sorteios_gerados.py', 'w', encoding='utf-8') as arquivo:
    arquivo.write('sorteios = {\n')
    for nome_sorteio, jogadores in sorteios.items():
        arquivo.write(f"    '{nome_sorteio}': [\n")
        for jogador in jogadores:
            arquivo.write(f"        {jogador},\n")
        arquivo.write('    ],\n')
    arquivo.write('}\n')

print("Sorteios gerados com sucesso! Verifique o arquivo 'sorteios_gerados.py'") 