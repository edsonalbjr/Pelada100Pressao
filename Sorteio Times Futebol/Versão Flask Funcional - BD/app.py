# chatgpt responda em pt-br esse é o app.py
import os
import unicodedata
from random import shuffle
import random
import pandas as pd
from flask import Flask, render_template, session, redirect, url_for, render_template_string, request, jsonify
from openpyxl import Workbook
from datetime import datetime
from glob import glob
from collections import defaultdict

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Número máximo de timesSorteio Times Futebol/Lista de Jogadores/bancodedados.xlsx
NUM_MAX_TIMES = 5

# Número máximo de jogadores por time
JOGADORES_POR_TIME = 6

# Número máximo de jogadores na lista de jogadores para sorteio
QTD_MAX_JOGADORES_SORTEIO = NUM_MAX_TIMES * JOGADORES_POR_TIME


# Carregando o arquivo Excel
file_path = "bancodedados.xlsx"
df = pd.read_excel(file_path)

# Substituindo os valores nan por None
df = df.where(pd.notna(df), None)

# Convertendo os dados filtrados para o formato desejado
jogadores = [
    {
        "id": jogador["id"],
        "nome": unicodedata.normalize('NFKD', str(jogador["jogador"])),
        "habilidade": int(jogador["habilidade"]) if pd.notna(jogador["habilidade"]) and jogador["habilidade"].is_integer() else jogador["habilidade"],
        "posicao_primaria": unicodedata.normalize('NFKD', str(jogador["posicao_primaria"])),
        "posicao_secundaria": unicodedata.normalize('NFKD', str(jogador["posicao_secundaria"])),
        "adm": True if unicodedata.normalize('NFKD', str(jogador["diretor"])) == 'sim' else False,
        "filiacao": unicodedata.normalize('NFKD', str(jogador["filiacao"])),
    }
    for _, jogador in df.iterrows()
]

# Distribuir jogadores nos dicionários adequados (mensalistas ou diaristas)
mensalistas = []
diaristas = []

for jogador in jogadores:
    if jogador["filiacao"] == "mensalista":
        mensalistas.append(jogador)
    elif jogador["filiacao"] == "diarista":
        diaristas.append(jogador)

# Lista de jogadores para sorteio
jogadores_sorteio = []


# Adiciona todos os mensalistas à lista de jogadores para sorteio
jogadores_sorteio.extend(mensalistas)

# Limpa a lista de mensalistas
mensalistas.clear()


@app.route('/')
def index():
    return render_template('index.html', mensalistas=mensalistas, diaristas=diaristas, jogadores_sorteio=jogadores_sorteio)


@app.route('/adicionar_mensalista/<int:index>', methods=['POST'])
def adicionar_mensalista(index):
    if len(jogadores_sorteio) >= QTD_MAX_JOGADORES_SORTEIO:
        return render_template('index.html', mensalistas=mensalistas, diaristas=diaristas, jogadores_sorteio=jogadores_sorteio) + "<script>alert('Limite de jogadores atingido');</script>"

    # Remove o mensalista da lista de mensalistas
    mensalista = mensalistas.pop(index)
    # Adiciona o mensalista à lista de jogadores para sorteio
    jogadores_sorteio.append(mensalista)
    return render_template('index.html', mensalistas=mensalistas, diaristas=diaristas, jogadores_sorteio=jogadores_sorteio)


@app.route('/adicionar_diarista/<int:index>', methods=['POST'])
def adicionar_diarista(index):
    if len(jogadores_sorteio) >= QTD_MAX_JOGADORES_SORTEIO:
        return render_template('index.html', mensalistas=mensalistas, diaristas=diaristas, jogadores_sorteio=jogadores_sorteio) + "<script>alert('Limite de jogadores atingido');</script>"

    diarista = diaristas.pop(index)  # Remove o diarista da lista de diaristas
    # Adiciona o diarista à lista de jogadores para sorteio
    jogadores_sorteio.append(diarista)
    return render_template('index.html', mensalistas=mensalistas, diaristas=diaristas, jogadores_sorteio=jogadores_sorteio)


@app.route('/remover_jogador/<int:index>', methods=['POST'])
def remover_jogador(index):
    # Remove o jogador da lista de jogadores para sorteio
    jogador = jogadores_sorteio.pop(index)

    # Verifica a filiação do jogador
    if jogador['filiacao'] == 'mensalista':
        mensalistas.append(jogador)
    elif jogador['filiacao'] == 'diarista':
        diaristas.append(jogador)

    return render_template('index.html', mensalistas=mensalistas, diaristas=diaristas, jogadores_sorteio=jogadores_sorteio)


@app.route('/sortear', methods=['POST'])
def sortear_times():
    # Verificar se há jogadores suficientes para realizar o sorteio
    if len(jogadores_sorteio) < QTD_MAX_JOGADORES_SORTEIO:
        # Calcular quantos jogadores faltam para atingir a quantidade mínima necessária
        faltam = QTD_MAX_JOGADORES_SORTEIO - len(jogadores_sorteio)
        # Criar a mensagem de alerta
        alerta = f"A quantidade de jogadores para o sorteio é insuficiente. Faltam {
            faltam} jogador(es) para atingir o mínimo necessário."
        # Retornar para a página inicial com o alerta e o script de alerta
        return render_template('index.html', mensalistas=mensalistas, diaristas=diaristas, jogadores_sorteio=jogadores_sorteio, alerta=alerta) + f"<script>alert('Faltam {faltam} jogador(es) para realizar o sorteio.');</script>"

    # Embaralhar a ordem dos times
    times = criar_times(jogadores_sorteio, NUM_MAX_TIMES)
    shuffle(times)

    # Armazenar os times na sessão
    session['times'] = times

    # Criar DataFrame com os dados dos times sorteados
    df_times = pd.DataFrame(columns=[
        'id', 'jogador', 'habilidade', 'posicao_primaria', 'posicao_secundaria',
        'filiacao', 'diretor', 'jogos', 'vitorias', 'empates', 'derrotas',
        'gols', 'assistencias', 'cartao_amarelo', 'cartao_vermelho', 'desistiu', 'substituicao', 'time', 'data'
    ])

    # Preencher o DataFrame com os dados dos times sorteados
    for i, time in enumerate(times, start=1):
        for jogador in time['jogadores']:
            # Calcular o número de jogos
            num_jogos = jogador.get(
                'vitorias', 0) + jogador.get('empates', 0) + jogador.get('derrotas', 0)

            jogador_data = {
                "id": jogador["id"],
                'jogador': jogador['nome'],
                'habilidade': jogador['habilidade'],
                'posicao_primaria': jogador['posicao_primaria'],
                'posicao_secundaria': jogador['posicao_secundaria'],
                'filiacao': jogador['filiacao'],
                'diretor': 'Sim' if jogador['adm'] else 'Não',
                'jogos': num_jogos,  # Valor calculado
                'vitorias': jogador.get('vitorias', ''),
                'empates': jogador.get('empates', ''),
                'derrotas': jogador.get('derrotas', ''),
                'gols': '',
                'assistencias': '',
                'cartao_amarelo': '',
                'cartao_vermelho': '',
                'desistiu': 'Não',
                'substituicao': [],
                'time': i,
                'data': datetime.now().strftime("%d-%m-%Y")
            }
            df_times = pd.concat(
                [df_times, pd.DataFrame([jogador_data])], ignore_index=True)

    # Obter o diretório atual
    diretorio_atual = os.getcwd()

    # Criar o caminho para a pasta "historico"
    diretorio_historico = os.path.join(diretorio_atual, 'historico')

    # Verificar se a pasta "historico" existe, se não, criar
    if not os.path.exists(diretorio_historico):
        os.makedirs(diretorio_historico)

    # Salvar o DataFrame em um arquivo Excel dentro da pasta "historico"
    file_name = f"pelada-{datetime.now().strftime('%d-%m-%Y')}.xlsx"
    file_path = os.path.join(diretorio_historico, file_name)

    # Verificar se o arquivo já existe e, em caso afirmativo, sobrescrever os dados
    if os.path.exists(file_path):
        os.remove(file_path)
    df_times.to_excel(file_path, index=False)

    # Redirecionar para a página de resultado do sorteio
    return redirect(url_for('resultado_sorteio'))


@app.route('/resultado_sorteio')
def resultado_sorteio():
    # Recuperar os times da sessão
    times = session.pop('times', None)
    if not times:
        return 'Não foi possível recuperar os times do sorteio.'

    # Atribuir o número de time após o embaralhamento
    for i, time in enumerate(times, start=1):
        for jogador in time['jogadores']:
            # Armazenar o número do time de cada jogador após o embaralhamento
            jogador['time'] = i

    return render_template('resultado_sorteio.html', times=times)


def criar_times(jogadores, num_times):
    # Verifica se há jogadores suficientes para formar os times
    total_jogadores = len(jogadores)
    if total_jogadores < num_times * JOGADORES_POR_TIME:
        return None  # Retorna None se não houver jogadores suficientes

    # Faz uma cópia aleatória da lista de jogadores
    jogadores_copia = random.sample(jogadores, len(jogadores))

    # Separar jogadores com 'adm': True e 'adm': False
    jogadores_adm_true = [j for j in jogadores_copia if j['adm']]
    jogadores_adm_false = [j for j in jogadores_copia if not j['adm']]

    # Ordenar ambos os grupos por habilidade de forma decrescente
    jogadores_adm_true = sorted(
        jogadores_adm_true, key=lambda x: x["habilidade"], reverse=True)
    jogadores_adm_false = sorted(
        jogadores_adm_false, key=lambda x: x["habilidade"], reverse=True)

    # Inicializa os times como listas vazias
    times = [[] for _ in range(num_times)]

    # Distribui jogadores com 'adm': True primeiro
    for jogador in jogadores_adm_true:
        menor_time = min(times, key=lambda t: (
            sum(j["habilidade"] for j in t), count_positions(t, jogador)))

        menor_time.append(jogador)

        if jogador["posicao_primaria"] != "qualquer":
            jogadores.remove(jogador)

        if not jogadores:
            break

    # Distribui os jogadores com 'adm': False
    for jogador in jogadores_adm_false:
        if jogador["posicao_primaria"] == "qualquer":
            menor_time = min(times, key=lambda t: sum(
                j["habilidade"] for j in t))
            menor_time.append(jogador)
            if jogador["posicao_primaria"] != "qualquer":
                jogadores.remove(jogador)
            if not jogadores:
                break
        else:
            menor_time = min(times, key=lambda t: (
                sum(j["habilidade"] for j in t), count_positions(t, jogador)))

            menor_time.append(jogador)

            if jogador["posicao_primaria"] != "qualquer":
                jogadores.remove(jogador)

            if not jogadores:
                break

    # Formata as informações dos times para exibição
    times_formatados = []
    for i, time in enumerate(times, start=1):
        habilidade_total = sum(jogador['habilidade'] for jogador in time)
        habilidade_total = int(
            habilidade_total) if habilidade_total.is_integer() else habilidade_total

        posicoes_primarias = ', '.join(
            jogador['posicao_primaria'] for jogador in time)
        posicoes_secundarias = ', '.join(jogador['posicao_secundaria'] for jogador in time if
                                         jogador['posicao_secundaria'] != 'nenhum')

        time_formatado = {
            'numero_time': i,
            'habilidade_total': habilidade_total,
            'posicoes_primarias': posicoes_primarias,
            'posicoes_secundarias': posicoes_secundarias,
            'jogadores': time
        }
        times_formatados.append(time_formatado)

    return times_formatados


# Função auxiliar para contar a quantidade de jogadores em cada posição
def count_positions(time, jogador, posicao=None):
    count_primarias = sum(
        1 for j in time if j["posicao_primaria"] == jogador["posicao_primaria"])
    count_secundarias = sum(
        1 for j in time if j["posicao_secundaria"] == jogador["posicao_secundaria"])

    if posicao:
        count_primarias += 1 if jogador["posicao_primaria"] == posicao else 0
        count_secundarias += 1 if jogador["posicao_secundaria"] == posicao else 0

    return count_primarias + count_secundarias


# Defina a rota para exibir os dados do arquivo Excel mais recente
@app.route('/pelada')
def exibir_dados_pelada():
    # Caminho para a pasta "historico"
    diretorio_historico = "historico"

    # Encontrar o arquivo Excel mais recente na pasta "historico"
    files = glob(os.path.join(diretorio_historico, "*.xlsx"))
    if not files:
        return "Nenhum arquivo encontrado na pasta histórico."

    # Pegar o arquivo mais recente com base na data do nome do arquivo
    file_path = max(files, key=os.path.getctime)

    # Carregar o arquivo Excel
    df = pd.read_excel(file_path)

    # Agrupar os jogadores pelo valor na coluna "time"
    grouped_data = df.groupby('time')[['jogador', 'habilidade']].apply(
        lambda x: x.to_dict(orient='records')).to_dict()

    # Passar a variável NUM_MAX_TIMES para o template
    return render_template('pelada.html', grouped_data=grouped_data, NUM_MAX_TIMES=NUM_MAX_TIMES)


@app.route('/partida')
def partida():
    # Caminho para a pasta "historico"
    diretorio_historico = "historico"

    # Encontrar o arquivo Excel mais recente na pasta "historico"
    files = glob(os.path.join(diretorio_historico, "*.xlsx"))
    if not files:
        return "Nenhum arquivo encontrado na pasta histórico."

    # Pegar o arquivo mais recente com base na data do nome do arquivo
    file_path = max(files, key=os.path.getctime)

    # Carregar o arquivo Excel
    df = pd.read_excel(file_path)

    # Substituir NaN por 0 em todas as colunas numéricas
    df.fillna(0, inplace=True)

    # Filtrar jogadores que não desistiram
    df = df[df['desistiu'] == 'Não']

    # Agrupar os jogadores por time em um dicionário
    jogadores_por_time = defaultdict(list)
    for _, jogador in df.iterrows():
        time = jogador['time']
        jogadores_por_time[time].append(jogador.to_dict())

    # Ordenar os jogadores pelo valor da habilidade do maior para o menor
    for time, jogadores in jogadores_por_time.items():
        jogadores_por_time[time] = sorted(
            jogadores, key=lambda x: x['habilidade'], reverse=True)

    # Renderizar o template partida.html com os dados da partida
    return render_template('partida.html', jogadores_por_time=jogadores_por_time)


@app.route('/desistir', methods=['POST'])
def desistir():
    # Obtém o ID do jogador da solicitação POST
    jogador_id = request.form['data']

    # Caminho para o arquivo Excel mais recente na pasta "historico"
    diretorio_historico = 'historico'
    files = glob(os.path.join(diretorio_historico, "*.xlsx"))
    if not files:
        return "Nenhum arquivo encontrado na pasta histórico."

    # Obtém o arquivo mais recente com base na data do nome do arquivo
    file_path = max(files, key=os.path.getctime)

    try:
        # Carrega os dados existentes do arquivo XLSX
        existing_data = pd.read_excel(file_path)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    # Atualiza o valor da coluna 'desistiu' para 'Sim' para o jogador com o ID correspondente
    existing_data.loc[existing_data['id'] ==
                      int(jogador_id), 'desistiu'] = 'Sim'

    # Escreve os dados atualizados no arquivo XLSX
    existing_data.to_excel(file_path, index=False)

    # Redireciona o usuário de volta para a página de partida
    return redirect(url_for('partida'))


@app.route('/acao', methods=['POST'])
def acao():
    # Obtém os dados enviados pelo formulário
    dados = request.form

    diretorio_historico = 'historico'
    # Caminho para o arquivo Excel mais recente na pasta "historico"
    files = glob(os.path.join(diretorio_historico, "*.xlsx"))
    if not files:
        return "Nenhum arquivo encontrado na pasta histórico."

    # Obtém o arquivo mais recente com base na data do nome do arquivo
    file_path = max(files, key=os.path.getctime)

    try:
        # Carrega os dados existentes do arquivo XLSX
        existing_data = pd.read_excel(file_path)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    # Verifica se a coluna 'id' existe no DataFrame existing_data
    if 'id' in existing_data.columns:
        jogador_id = dados.get('id')

        # Verifica a ação solicitada e atualiza os dados conforme necessário
        if 'gol' in dados:
            existing_data.loc[existing_data['id']
                              == int(jogador_id), 'gols'] += 1
        elif 'gol_contra' in dados:
            existing_data.loc[existing_data['id']
                              == int(jogador_id), 'gols'] -= 1
        elif 'assistencia' in dados:
            existing_data.loc[existing_data['id'] ==
                              int(jogador_id), 'assistencias'] += 1
        elif 'cartao_amarelo' in dados:
            existing_data.loc[existing_data['id'] ==
                              int(jogador_id), 'cartao_amarelo'] += 1
        elif 'cartao_vermelho' in dados:
            existing_data.loc[existing_data['id'] ==
                              int(jogador_id), 'cartao_vermelho'] += 1

        # Escreve os dados atualizados no arquivo XLSX
        existing_data.to_excel(file_path, index=False)

    # Redireciona de volta para a página de partida após a execução da ação
    return redirect(url_for('partida'))


if __name__ == '__main__':
    app.run(debug=True)
