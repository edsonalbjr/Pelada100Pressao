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
                        if isinstance(summed_data[player_name].get(key), str):
                            summed_data[player_name][key] = str(
                                float(summed_data[player_name][key]) + value)
                        else:
                            summed_data[player_name][key] += value
            else:
                summed_data[player_name] = row.copy()

        # Calcular o aproveitamento para cada jogador
        for player_data in summed_data.values():
            vitorias = player_data['Vitórias']
            empates = player_data['Empate']
            jogos = player_data['Jogos']

            # Verificar se o número de jogos é diferente de zero
            if jogos != 0:
                aproveitamento = (vitorias + (empates / 2)) / jogos
                player_data['Aproveitamento'] = f"{aproveitamento * 100:.2f}%"
            else:
                player_data['Aproveitamento'] = "N/A"

        # Calcular o percentual de gols por jogo para cada jogador
        for player_data in summed_data.values():
            gols = player_data['Gols']
            jogos = player_data['Jogos']

            # Verificar se o número de jogos é diferente de zero
            if jogos != 0:
                percent_gols_por_jogo = (gols / jogos) * 100
                player_data['%G/J'] = f"{percent_gols_por_jogo:.2f}%"
            else:
                player_data['%G/J'] = "N/A"

        # Calcular o percentual de assistências por jogo para cada jogador
        for player_data in summed_data.values():
            assistencias = player_data['Assistências']
            jogos = player_data['Jogos']

            # Verificar se o número de jogos é diferente de zero
            if jogos != 0:
                percent_assistencias_por_jogo = (assistencias / jogos) * 100
                player_data['%A/J'] = f"{percent_assistencias_por_jogo:.2f}%"
            else:
                player_data['%A/J'] = "N/A"

        # Calcular o percentual de participações em gols por jogo para cada jogador
        for player_data in summed_data.values():
            participacoes_gols = player_data['Participações em gols']
            jogos = player_data['Jogos']

            # Verificar se o número de jogos é diferente de zero
            if jogos != 0:
                percent_participacoes_gols_por_jogo = (
                    participacoes_gols / jogos) * 100
                player_data['%P/G'] = f"{percent_participacoes_gols_por_jogo:.2f}%"
            else:
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
