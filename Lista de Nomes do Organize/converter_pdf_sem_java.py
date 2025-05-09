import pandas as pd
import pdfplumber
import re
import os
from collections import Counter

# Define os caminhos dos arquivos
pdf_path = "Organizze.pdf"
txt_path = "Organizze.txt"

# Abre o arquivo PDF
print("Extraindo nomes do PDF...")
dados_extraidos = []

with pdfplumber.open(pdf_path) as pdf:
    num_paginas = len(pdf.pages)
    print(f"O PDF tem {num_paginas} páginas.")
    
    for i, pagina in enumerate(pdf.pages):
        texto = pagina.extract_text()
        if texto:
            print(f"Processando página {i+1}/{num_paginas}")
            
            # Divide o texto em linhas
            linhas = texto.split('\n')
            for linha in linhas:
                linha = linha.strip()
                
                # Procura por linhas que começam com 'receita' ou 'despesa'
                if re.match(r'^(receita|despesa)', linha, re.IGNORECASE):
                    # Nova abordagem: captura qualquer texto entre a data e 'Conta' ou 'Carteira'
                    # Formato da data: dd/mm/aaaa
                    match = re.search(r'\b(\d{2}/\d{2}/\d{4})\s+(.+?)\s+(Conta|Carteira)\b', linha, re.IGNORECASE)
                    
                    if match:
                        data = match.group(1)       # a data
                        descricao = match.group(2)  # o nome/descrição que queremos
                        tipo_conta = match.group(3) # 'Conta' ou 'Carteira'
                        
                        # Limpa a descrição de quaisquer espaços extras
                        descricao = descricao.strip()
                        
                        # Adiciona a descrição limpa aos dados extraídos
                        if descricao:
                            dados_extraidos.append(descricao)
                            print(f"Encontrado: '{descricao}' (entre {data} e {tipo_conta})")

# Se não encontramos nada com o método acima, tentar um método mais simples
if not dados_extraidos:
    print("Padrão não encontrado, tentando método alternativo...")
    with pdfplumber.open(pdf_path) as pdf:
        for i, pagina in enumerate(pdf.pages):
            texto = pagina.extract_text()
            if texto:
                linhas = texto.split('\n')
                for linha in linhas:
                    # Procura qualquer data seguida por algum texto antes de 'Conta' ou 'Carteira'
                    match = re.search(r'\d{2}/\d{2}/\d{4}\s+([^C]+?)\s+(Conta|Carteira)', linha)
                    if match:
                        descricao = match.group(1).strip()
                        if descricao:
                            dados_extraidos.append(descricao)
                            print(f"Método alternativo: '{descricao}'")

# Conta as ocorrências de cada descrição
contador = Counter(dados_extraidos)

# Cria lista de descrições com contagem
descricoes_contadas = []
for descricao, contagem in contador.items():
    if contagem > 1:
        # Se aparece mais de uma vez, adiciona o contador
        descricoes_contadas.append([f"{descricao} ({contagem})", contagem])
    else:
        # Se aparece apenas uma vez, não precisa do contador
        descricoes_contadas.append([descricao, contagem])

# Ordena do maior para o menor número de ocorrências
descricoes_contadas.sort(key=lambda x: x[1], reverse=True)

# Remove a contagem da lista final, mantendo apenas a descrição formatada
descricoes_formatadas = [item[0] for item in descricoes_contadas]

# Salva em um arquivo de texto
try:
    print(f"\nTotal de descrições únicas: {len(descricoes_formatadas)}")
    print(f"Salvando dados em {txt_path}...")
    
    with open(txt_path, 'w', encoding='utf-8') as arquivo:
        # Adiciona um cabeçalho
        arquivo.write("DESCRIÇÕES DO ORGANIZZE\n")
        arquivo.write("=====================\n\n")
        
        # Escreve cada descrição em uma linha
        for descricao in descricoes_formatadas:
            arquivo.write(f"{descricao}\n")
            
    print(f"Arquivo de texto salvo como '{txt_path}'")
except Exception as e:
    print(f"Erro ao salvar o arquivo de texto: {e}")

print("\nAs descrições foram agrupadas, contadas e ordenadas do maior para o menor número de ocorrências.") 