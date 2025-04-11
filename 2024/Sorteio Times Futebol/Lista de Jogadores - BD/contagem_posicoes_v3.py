# Importando as listas de jogadores do arquivo original
from lista_de_jogadores import mensalistas, diaristas

# Função para classificar jogadores por posição
def classificar_por_posicao():
    # Criando os grupos de posições
    grupos = {
        'zagueiro': [],
        'zagueiro/meia': [],
        'zagueiro/atacante': [],
        'meia': [],
        'meia/zagueiro': [],
        'meia/atacante': [],
        'atacante': [],
        'atacante/meia': [],
        'atacante/zagueiro': [],
        'qualquer': []
    }
    
    # Combinando as duas listas de jogadores
    todos_jogadores = mensalistas + diaristas
    
    # Classificando cada jogador no grupo apropriado
    for jogador in todos_jogadores:
        nome = jogador['nome']
        pos_primaria = jogador['posicao_primaria']
        pos_secundaria = jogador['posicao_secundaria']
        
        # Jogadores com posição "qualquer"
        if pos_primaria == 'qualquer':
            grupos['qualquer'].append({'nome': nome, 'posicao': 'qualquer'})
            continue
            
        # Jogadores sem posição secundária ou com secundária "nenhum"
        if pos_secundaria == 'nenhum' or not pos_secundaria:
            grupos[pos_primaria].append({'nome': nome, 'posicao': pos_primaria})
        else:
            # Jogadores com posição primária e secundária
            grupo_chave = f"{pos_primaria}/{pos_secundaria}"
            # Verificar se o grupo existe, senão usar apenas a posição primária
            if grupo_chave in grupos:
                grupos[grupo_chave].append({'nome': nome, 'posicao': grupo_chave})
            else:
                grupos[pos_primaria].append({'nome': nome, 'posicao': f"{pos_primaria}/{pos_secundaria}"})
    
        # Ordenar cada grupo em ordem alfabética pelo nome do jogador
        for grupo in grupos:
            grupos[grupo].sort(key=lambda x: x['nome'].lower())

    return grupos

# Exibir os jogadores por grupo
def exibir_grupos():
    grupos = classificar_por_posicao()
    
    print("=== JOGADORES POR POSIÇÃO ===\n")
    
    # Ordem de exibição dos grupos
    ordem_grupos = [
        'zagueiro', 
        'zagueiro/meia', 
        'zagueiro/atacante',
        'meia', 
        'meia/zagueiro', 
        'meia/atacante',
        'atacante', 
        'atacante/meia', 
        'atacante/zagueiro',
        'qualquer'
    ]
    
    for grupo in ordem_grupos:
        if grupos[grupo]:
            print(f"*{grupo.upper()}*")
            # Extrair apenas os nomes dos jogadores
            nomes_jogadores = [jogador['nome'] for jogador in grupos[grupo]]
            # Juntar os nomes com vírgulas
            lista_nomes = ", ".join(nomes_jogadores)
            print(lista_nomes)
            print()  # Linha em branco após cada grupo

# Executar o programa
if __name__ == "__main__":
    exibir_grupos()
