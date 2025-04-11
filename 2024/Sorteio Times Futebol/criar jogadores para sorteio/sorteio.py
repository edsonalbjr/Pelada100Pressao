def ler_arquivo_jogadores(caminho_arquivo):
    jogadores = []
    erros = []  # Lista para armazenar logs de erro

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha_numero, linha in enumerate(arquivo, 1):
                try:
                    dados = linha.strip().split('\t')
                    if len(dados) != 4:
                        raise ValueError("Número incorreto de colunas.")

                    nome, habilidade, posicao_primaria, posicao_secundaria = dados
                    habilidade = habilidade.replace(',', '.')  # Substitui vírgula por ponto
                    
                    try:
                        habilidade_float = float(habilidade)
                    except ValueError:
                        raise ValueError(f"Valor de habilidade inválido: '{habilidade}' não é um número válido.")

                    # Se a habilidade é um número inteiro, mantemos como inteiro
                    habilidade_final = int(habilidade_float) if habilidade_float.is_integer() else habilidade_float

                    jogador = {
                        'nome': nome,
                        'habilidade': habilidade_final,
                        'posicao_primaria': posicao_primaria,
                        'posicao_secundaria': posicao_secundaria,
                        'adm': False
                    }
                    jogadores.append(jogador)
                except Exception:
                    erros.append(f"Erro na linha {linha_numero}")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return []

    except Exception as e:
        print(f"Erro geral ao ler o arquivo: {e}")
        return []

    if erros:
        print(f"Ocorreram {len(erros)} erros de formatação no arquivo.")
    else:
        print("Arquivo lido com sucesso!")

    return jogadores

# Exemplo de uso:
caminho_arquivo = 'jogadores.txt'
jogadores = ler_arquivo_jogadores(caminho_arquivo)

for jogador in jogadores:
    print(jogador)
