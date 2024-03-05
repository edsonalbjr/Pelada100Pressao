from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

data = []  # Lista para armazenar os dados de todos os arquivos enviados


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificar se um arquivo foi enviado
        if 'file' not in request.files:
            return "Nenhum arquivo enviado."

        # Obter a lista de arquivos enviados
        files = request.files.getlist('file')

        # Percorrer todos os arquivos enviados
        for file in files:
            # Verificar se o arquivo tem uma extensão válida
            if file.filename == '':
                return "Nenhum arquivo selecionado."

            if file:
                # Ler o arquivo Excel usando o pandas
                df = pd.read_excel(file)

                # Converter o DataFrame em uma lista de dicionários
                file_data = df.to_dict('records')

                # Adicionar os dados do arquivo à lista geral de dados
                data.extend(file_data)

        # Somar os valores das estatísticas para jogadores com o mesmo nome
        summed_data = {}
        for row in data:
            player_name = row['Nome']
            if player_name in summed_data:
                for key, value in row.items():
                    if key != 'Nome':
                        existing_value = summed_data[player_name].get(key)

                        # Check if the existing value is a numeric type
                        if isinstance(existing_value, (int, float)):
                            # Try to convert the new value to float, handle exceptions
                            try:
                                float_value = float(value)
                            except ValueError:
                                print(f"Could not convert '{
                                      value}' to float for key {key}")
                                continue

                            # Add the float values
                            summed_data[player_name][key] = existing_value + \
                                float_value
                        elif isinstance(existing_value, str) and existing_value.isdigit():
                            # If the existing value is a string representing an integer, convert both and add
                            summed_data[player_name][key] = int(
                                existing_value) + int(value)
                        else:
                            # Handle other cases or raise an error if needed
                            print(f"Unexpected value type for key {
                                  key}: {existing_value}")

                        # Handle the case when 'Participações em gols' column is not present in the old data
                        if 'Participações em gols' not in summed_data[player_name]:
                            summed_data[player_name]['Participações em gols'] = 0

                        # Handle the case when '%P/G' column is not present in the old data
                        if '%P/G' not in summed_data[player_name]:
                            summed_data[player_name]['%P/G'] = "N/A"
            else:
                summed_data[player_name] = row.copy()

        # Calcular o aproveitamento para cada jogador
        for player_data in summed_data.values():
            vitorias = player_data['Vitórias']
            empates = player_data['Empate']
            jogos = player_data['Jogos']

            # Verificar se o número de jogos é diferente de zero
            if jogos != 0:
                aproveitamento = (vitorias + empates) / jogos
                player_data['Aproveitamento'] = f"{
                    round(aproveitamento * 100, 1)}%"
            else:
                player_data['Aproveitamento'] = "N/A"

        # Formatar os valores inteiros para não exibir a parte decimal
        for player_data in summed_data.values():
            for key, value in player_data.items():
                if isinstance(value, float) and value.is_integer():
                    player_data[key] = int(value)

        # Calcular o percentual de gols por jogo para cada jogador
        for player_data in summed_data.values():
            gols = player_data['Gols']
            jogos = player_data['Jogos']

            # Verificar se o número de jogos é diferente de zero
            if jogos != 0:
                percent_gols_por_jogo = (gols / jogos) * 100
                player_data['%G/J'] = f"{round(percent_gols_por_jogo, 1)
                                         }%"
            else:
                player_data['%G/J'] = "N/A"

        # Calcular o percentual de assistências por jogo para cada jogador
        for player_data in summed_data.values():
            assistencias = player_data['Assistências']
            jogos = player_data['Jogos']

            # Verificar se o número de jogos é diferente de zero
            if jogos != 0:
                percent_assistencias_por_jogo = (assistencias / jogos) * 100
                player_data['%A/J'] = f"{
                    round(percent_assistencias_por_jogo, 1)}%"
            else:
                player_data['%A/J'] = "N/A"

        # Calcular o percentual de participações em gols por jogo para cada jogador
        for player_data in summed_data.values():
            gols = player_data['Gols']
            assistencias = player_data['Assistências']
            jogos = player_data['Jogos']

            # Verificar se o número de jogos é diferente de zero
            if jogos != 0:
                participacoes_gols = gols + assistencias
                percent_participacoes_gols_por_jogo = (
                    participacoes_gols / jogos) * 100
                player_data['Participações em gols'] = participacoes_gols
                player_data['%P/G'] = f"{
                    round(percent_participacoes_gols_por_jogo, 1)}%"
            else:
                player_data['Participações em gols'] = 0
                player_data['%P/G'] = "N/A"

        # Converter os dados somados em uma lista para exibição
        summed_data = list(summed_data.values())

        # Ordenar os dados por pontuação em ordem decrescente
        summed_data.sort(key=lambda x: x['Pontos'], reverse=True)

        # Obter os 10 maiores pontuadores
        maiores_pontuadores = summed_data[:10]

        # Obter os 10 jogadores com mais jogos
        maiores_jogos = sorted(
            summed_data, key=lambda x: x['Jogos'], reverse=True)[:10]

        # Obter os 10 artilheiros
        artilheiros = sorted(
            summed_data, key=lambda x: x['Gols'], reverse=True)[:10]

        # Obter os 10 jogadores com maior %G/J
        percent_gols_por_jogo = sorted(
            summed_data, key=lambda x: float(x['%G/J'][:-1]) if x['%G/J'] != 'N/A' else -1, reverse=True)[:10]

        # Obter os 10 jogadores com mais assistências
        assistencias = sorted(
            summed_data, key=lambda x: x['Assistências'], reverse=True)[:10]

        # Obter os 10 jogadores com maior %A/J
        percent_assistencias_por_jogo = sorted(
            summed_data, key=lambda x: float(x['%A/J'][:-1]) if x['%A/J'] != 'N/A' else -1, reverse=True)[:10]

        # Obter os 10 jogadores com maior %P/G
        percent_participacoes_gols_por_jogo = sorted(
            summed_data, key=lambda x: float(x['%P/G'][:-1]) if x['%P/G'] != 'N/A' else -1, reverse=True)[:10]

        # Obter os 10 jogadores com mais participações em gols
        participacoes_gols = sorted(
            summed_data, key=lambda x: x['Participações em gols'], reverse=True)[:10]

        # Obter os 10 jogadores com mais vitórias
        vitorias = sorted(
            summed_data, key=lambda x: x['Vitórias'], reverse=True)[:10]

        # Obter os 10 jogadores com mais derrotas
        derrotas = sorted(
            summed_data, key=lambda x: x['Derrotas'], reverse=True)[:10]

        # Obter os 10 jogadores com mais empates
        empate = sorted(
            summed_data, key=lambda x: x['Empate'], reverse=True)[:10]

        # Obter os 10 jogadores com melhores aproveitamentos
        aproveitamento = sorted(
            summed_data,
            key=lambda x: float(x['Aproveitamento'][:-1]
                                ) if x['Aproveitamento'] != "N/A" else -1,
            reverse=True
        )[:10]

        # Obter os 10 jogadores com maior C/A (Cartão Amarelo)
        c_a = sorted(summed_data, key=lambda x: x['C/A'], reverse=True)[:10]

        # Obter os 10 jogadores com maior C/V (Cartão Vermelho)
        c_v = sorted(summed_data, key=lambda x: x['C/V'], reverse=True)[:10]

        # Renderizar o template HTML e passar os dados para exibição
        return render_template('tabela.html', data=summed_data, maiores_pontuadores=maiores_pontuadores,
                               maiores_jogos=maiores_jogos, artilheiros=artilheiros,
                               percent_gols_por_jogo=percent_gols_por_jogo, assistencias=assistencias,
                               percent_assistencias_por_jogo=percent_assistencias_por_jogo,
                               participacoes_gols=participacoes_gols,
                               percent_participacoes_gols_por_jogo=percent_participacoes_gols_por_jogo,
                               vitorias=vitorias, derrotas=derrotas, empate=empate, aproveitamento=aproveitamento, c_a=c_a, c_v=c_v)
    else:
        return render_template('tabela.html')


if __name__ == '__main__':
    app.run()
