from flask import Flask, render_template, request
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Lista de colunas a serem somadas
columns_to_sum = [
    'Pontos', 'Jogos', 'Gols', 'Assistências', 'Participações em gols',
    'Vitórias', 'Derrotas', 'Empate', 'Aproveitamento', 'C/A', 'C/V'
]

# Ler os dados do Excel


def read_excel_data(folder_path):
    all_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):
            filepath = os.path.join(folder_path, filename)
            # Especificar o separador decimal
            df = pd.read_excel(filepath, decimal=',')
            # Substituir valores nan por 0
            df.fillna(0, inplace=True)
            all_data.append(df)

    # Concatenar todos os dataframes em um único dataframe
    df_combined = pd.concat(all_data, ignore_index=True)
    return df_combined


@app.route('/')
def dashboard():
    folder_path = 'pasta_com_os_excel'  # substitua pelo caminho da sua pasta
    df = read_excel_data(folder_path)
    # Tratar valores não finitos
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)
    # Converter as colunas para números inteiros
    int_columns = [
        'Pontos', 'Jogos', 'Gols', 'Assistências', 'Participações em gols',
        'Vitórias', 'Derrotas', 'Empate', 'C/A', 'C/V'
    ]
    for col in int_columns:
        df[col] = df[col].astype(int)
    # Calcular a soma das colunas para cada jogador
    summed_data = df.groupby('Nome')[int_columns].sum().reset_index()
    dashboard_data = {row['Nome']: row.to_dict()
                      for _, row in summed_data.iterrows()}
    # Filtrar os dados
    filtered_dashboard_data = filter_dashboard_data(dashboard_data)
    return render_template('dashboard.html', dashboard_data=filtered_dashboard_data)


@app.route('/perfil/<string:player_name>')
def player_profile(player_name):
    folder_path = 'pasta_com_os_excel'  # substitua pelo caminho da sua pasta
    df = read_excel_data(folder_path)
    # Converter o nome do jogador para lowercase
    player_name_lower = player_name.lower()
    # Filtrar os dados para obter o perfil do jogador
    player_data = df[df['Nome'].str.lower(
    ) == player_name_lower].iloc[0].to_dict()
    return render_template('perfil.html', player_data=player_data)


def filter_dashboard_data(dashboard_data):
    filtered_data = {}
    for player, data in dashboard_data.items():
        if any(value != 0 for value in data.values()):
            filtered_data[player] = data
    return filtered_data


@app.route('/comparacao', methods=['GET', 'POST'])
def comparison():
    folder_path = 'pasta_com_os_excel'  # substitua pelo caminho da sua pasta
    df = read_excel_data(folder_path)

    # Filtrar e ordenar jogadores alfabeticamente
    players = sorted([str(name) for name in df['Nome'].unique(
    ).tolist() if not str(name).isdigit()], key=lambda x: x.lower())

    if request.method == 'POST':
        player1 = request.form['player1']
        player2 = request.form['player2']

        # Filtrar dados dos jogadores selecionados
        player_data1 = df[df['Nome'] ==
                          player1].iloc[0][columns_to_sum].to_dict()
        player_data2 = df[df['Nome'] ==
                          player2].iloc[0][columns_to_sum].to_dict()

        return render_template('comparacao.html', players=players, player1=player1, player2=player2, player_data1=player_data1, player_data2=player_data2)

    return render_template('comparacao.html', players=players)


@app.template_filter('int_or_none')
def int_or_none(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


if __name__ == '__main__':
    app.run(debug=True)
