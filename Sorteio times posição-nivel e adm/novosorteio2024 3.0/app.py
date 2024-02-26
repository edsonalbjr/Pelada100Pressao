from flask import Flask, render_template, request, redirect, url_for
from collections import Counter
import random
import pandas as pd

app = Flask(__name__)

# Lista de jogadores
jogadores = []

# Carregar dados do banco de dados
db_path = 'bancodedados.xlsx'
dados = pd.read_excel(db_path)

# Converter dados do DataFrame para lista de dicionários
jogadores_db = dados.to_dict(orient='records')

# Conjunto para armazenar IDs dos jogadores adicionados
jogadores_adicionados = set()

# Lista de jogadores para sorteio
jogadores_para_sorteio = []

# Rota principal para exibir a lista de jogadores e botões


def formatar_valor(valor):
    # Função para formatar a primeira letra de cada palavra em maiúscula
    if valor:
        return ' '.join(word.capitalize() for word in valor.split('_'))
    else:
        return valor

# Rota principal para exibir a lista de jogadores e botões


@app.route('/')
def index():
    # Aplicar a formatação aos valores antes de passá-los para o template
    jogadores_formatados = []
    for jogador in jogadores_db:
        jogador_formatado = {
            'jogador': formatar_valor(jogador['jogador']),
            'habilidade': jogador['habilidade'],
            'posicao_primaria': formatar_valor(jogador['posicao_primaria']),
            'posicao_secundaria': formatar_valor(jogador['posicao_secundaria']),
            'filiacao': formatar_valor(jogador['filiacao']),
            'diretor': formatar_valor(jogador['diretor']),
        }
        jogadores_formatados.append(jogador_formatado)

    return render_template('index.html', jogadores=jogadores_formatados, jogadores_para_sorteio=jogadores_para_sorteio)


# Rota para adicionar jogador à lista de jogadores para sorteio


@app.route('/adicionar_jogador/<int:jogador_id>', methods=['GET', 'POST'])
def adicionar_jogador(jogador_id):
    global jogadores_para_sorteio

    jogador_selecionado = next(
        (jogador for jogador in jogadores_db if jogador['id'] == jogador_id), None)

    if jogador_selecionado:
        if jogador_id in jogadores_adicionados:
            # Remover o jogador se já estiver na lista
            jogadores.remove(jogador_selecionado)
            jogadores_adicionados.remove(jogador_id)
            jogadores_para_sorteio.remove(jogador_selecionado)
        else:
            # Adicionar o jogador se não estiver na lista
            jogadores.append(jogador_selecionado)
            jogadores_adicionados.add(jogador_id)
            jogadores_para_sorteio.append(jogador_selecionado)

        # Limitar a lista de jogadores para sorteio a 25 jogadores
        jogadores_para_sorteio = jogadores_para_sorteio[-25:]

    return render_template('index.html', jogadores=jogadores_db, jogadores_para_sorteio=jogadores_para_sorteio)


# Rota para sortear os times


# Rota para sortear os times
@app.route('/sortear_times')
def sortear_times():
    # Se já houver jogadores, limpa a lista antes de sortear novamente
    if jogadores:
        jogadores.clear()

    # Implemente aqui a lógica de sortear times usando a função criar_times()
    num_times = 5  # Ajuste o número de times conforme necessário
    times_sorteados = criar_times(jogadores_para_sorteio, num_times)

    # Exibir os times sorteados
    return render_template('times.html', times_sorteados=times_sorteados)


# Função para criar times com base nas habilidades e posições dos jogadores
def criar_times(jogadores, num_times):
    # Fazer uma cópia aleatória da lista de jogadores
    jogadores_copia = random.sample(jogadores, len(jogadores))

    # Separar jogadores com 'adm': True e 'adm': False
    jogadores_adm_true = [
        j for j in jogadores_copia if 'adm' in j and j['adm']]
    jogadores_adm_false = [
        j for j in jogadores_copia if 'adm' in j and not j['adm']]

    # Ordenar ambos os grupos por habilidade de forma decrescente
    jogadores_adm_true = sorted(
        jogadores_adm_true, key=lambda x: x.get("habilidade", 0), reverse=True)
    jogadores_adm_false = sorted(
        jogadores_adm_false, key=lambda x: x.get("habilidade", 0), reverse=True)

    # Inicializa os times como listas vazias
    times = [[] for _ in range(num_times)]

    # Distribui jogadores com 'adm': True primeiro
    for jogador in jogadores_adm_true:
        # Encontra o time com menor número de jogadores e posições equilibradas
        menor_time = min(times, key=lambda t: (
            sum(j["habilidade"] for j in t), count_positions(t, jogador)))

        # Adiciona o jogador ao time
        menor_time.append(jogador)

        # Remove o jogador da lista geral apenas se não for "Qualquer"
        if jogador["posicao_primaria"] != "Qualquer":
            jogadores.remove(jogador)

        # Verifica se todos os jogadores foram distribuídos
        if not jogadores:
            break

    # Distribui os jogadores com 'adm': False
    for jogador in jogadores_adm_false:
        # Se a posição primária for "Qualquer", distribui o jogador para o time com menor habilidade
        if jogador["posicao_primaria"] == "Qualquer":
            menor_time = min(times, key=lambda t: sum(
                j["habilidade"] for j in t))
            menor_time.append(jogador)
            if jogador["posicao_primaria"] != "Qualquer":
                jogadores.remove(jogador)
            if not jogadores:
                break
        else:
            # Encontra o time com menor número de jogadores e posições equilibradas
            menor_time = min(times, key=lambda t: (
                sum(j["habilidade"] for j in t), count_positions(t, jogador)))

            # Adiciona o jogador ao time
            menor_time.append(jogador)

            # Remove o jogador da lista geral apenas se não for "Qualquer"
            if jogador["posicao_primaria"] != "Qualquer":
                jogadores.remove(jogador)

            # Verifica se todos os jogadores foram distribuídos
            if not jogadores:
                break

    return times


# Exemplo de uso
jogadores = [
    {'nome': 'Claudino', 'habilidade': 5.0,
        'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'nenhum'},
    {'nome': 'Dudu', 'habilidade': 5.0, 'posicao_primaria': 'qualquer',
        'posicao_secundaria': 'nenhum'},
    # Adicione mais jogadores conforme necessário
]

num_times = 2  # Altere o número de times conforme necessário
times = criar_times(jogadores, num_times)

# Imprimir os times
for i, time in enumerate(times, 1):
    # print(f'Time {i} | Habilidade Total: {time["habilidade_total"]:.1f}')

    # Parte 1: Posições Primárias
    posicoes_primarias = time["posicoes_primarias"]
    formatted_posicoes_primarias = [
        f"{pos} ({qtd})" for pos, qtd in posicoes_primarias.items()]
    joined_posicoes_primarias = ", ".join(formatted_posicoes_primarias)
    # print(f"Posições Primárias: {joined_posicoes_primarias}")

    # Parte 2: Posições Secundárias
    posicoes_secundarias = time["posicoes_secundarias"]
    formatted_posicoes_secundarias = [
        f"{pos} ({qtd})" for pos, qtd in posicoes_secundarias.items()]
    joined_posicoes_secundarias = ", ".join(formatted_posicoes_secundarias)
    # print(f'Posições Secundárias: {joined_posicoes_secundarias}')

    # Parte 3: Jogadores
for jogador in time['jogadores']:
    jogador_info = (
        f'Jogador: {jogador["nome"]} | '
        f'Habilidade: {jogador["habilidade"]:.1f} | '
        f'Posição Primária: {jogador["posicao_primaria"]} | '
        f'Posição Secundária: {jogador["posicao_secundaria"]}'
    )
    # print(jogador_info)

    # print('\n')


# Executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
