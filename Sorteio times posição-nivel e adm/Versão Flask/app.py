from flask import Flask, render_template, request, redirect, url_for
from collections import Counter
from random import shuffle, random
import pandas as pd

app = Flask(__name__)

# Lista de jogadores
jogadores = []

# Carregar dados do banco de dados
db_path = 'bancodedados.xlsx'
dados = pd.read_excel(db_path)

# Utilizar o DataFrame diretamente
jogadores_db = dados.to_dict(orient='records')


# Conjunto para armazenar IDs dos jogadores adicionados
jogadores_adicionados = set()

# Lista de jogadores para sorteio
jogadores_para_sorteio = []

# Rota principal para exibir a lista de jogadores e botões


def formatar_valor(valor):
    return ' '.join(word.capitalize() for word in valor.split('_')) if valor else valor


def formatar_habilidade(habilidade):
    if habilidade % 1 == 0:
        return int(habilidade)
    return habilidade


# Adicione o filtro à sua aplicação Flask
app.jinja_env.filters['formatar_habilidade'] = formatar_habilidade


# Rota principal para exibir a lista de jogadores e botões


@app.route('/')
def index():
    jogadores_formatados = []

    for jogador in jogadores_db:
        jogador_formatado = {
            # Adicione o ID do jogador ao dicionário formatado
            'id': jogador['id'],
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


@app.route('/adicionar_jogador/<int:jogador_id>', methods=['POST'])
def adicionar_jogador(jogador_id):
    global jogadores_para_sorteio

    jogador_selecionado = next(
        (jogador for jogador in jogadores_db if jogador['id'] == jogador_id), None)

    if jogador_selecionado:
        if jogador_id not in jogadores_adicionados:
            jogadores.append(jogador_selecionado)
            jogadores_adicionados.add(jogador_id)
            jogadores_para_sorteio.append(jogador_selecionado)
            jogadores_para_sorteio = jogadores_para_sorteio[-25:]

    return render_template('index.html', jogadores=jogadores_db, jogadores_para_sorteio=jogadores_para_sorteio)


@app.route('/remover_jogador/<int:jogador_id>', methods=['POST'])
def remover_jogador(jogador_id):
    global jogadores_para_sorteio

    jogador_selecionado = next(
        (jogador for jogador in jogadores_db if jogador['id'] == jogador_id), None)

    if jogador_selecionado:
        if jogador_id in jogadores_adicionados:
            jogadores.remove(jogador_selecionado)
            jogadores_adicionados.remove(jogador_id)
            jogadores_para_sorteio.remove(jogador_selecionado)

    return render_template('index.html', jogadores=jogadores_db, jogadores_para_sorteio=jogadores_para_sorteio)


# Rota para sortear os times
@app.route('/sortear_times')
def sortear_times():
    # Se já houver jogadores, limpa a lista antes de sortear novamente
    if jogadores_para_sorteio:
        jogadores_para_sorteio.clear()

    # Implemente aqui a lógica de sortear times usando a função criar_times()
    num_times = 5  # Ajuste o número de times conforme necessário
    times_sorteados = criar_times(jogadores, num_times)

    # Exibir os times sorteados
    return render_template('times.html', times=times_sorteados)


def criar_times(jogadores, num_times):
    # Embaralhe a lista de jogadores para um sorteio mais justo
    shuffle(jogadores)

    # Divida a lista de jogadores em grupos com base no número de times
    jogadores_por_time = [jogadores[i::num_times] for i in range(num_times)]

    # Crie times com base nas posições primárias e secundárias dos jogadores
    times = []
    for i, jogadores_time in enumerate(jogadores_por_time, 1):
        time = {
            'nome': f'Time {i}',
            'jogadores': jogadores_time,
            'posicoes_primarias': {},
            'posicoes_secundarias': {},
            'habilidade_total': 0.0,
        }

        for jogador in jogadores_time:
            # Atualize as posições primárias
            posicao_primaria = jogador['posicao_primaria']
            time['posicoes_primarias'][posicao_primaria] = time['posicoes_primarias'].get(
                posicao_primaria, 0) + 1

            # Atualize as posições secundárias
            posicao_secundaria = jogador['posicao_secundaria']
            time['posicoes_secundarias'][posicao_secundaria] = time['posicoes_secundarias'].get(
                posicao_secundaria, 0) + 1

            # Calcule a habilidade total do time
            time['habilidade_total'] += float(jogador['habilidade'])

        # Adicione o time à lista de times
        times.append(time)

    return times


@app.route('/limpar_lista', methods=['POST'])
def limpar_lista():
    global jogadores, jogadores_adicionados, jogadores_para_sorteio
    jogadores.clear()
    jogadores_adicionados.clear()
    jogadores_para_sorteio.clear()
    return render_template('index.html', jogadores=jogadores_db, jogadores_para_sorteio=jogadores_para_sorteio)


# Executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
