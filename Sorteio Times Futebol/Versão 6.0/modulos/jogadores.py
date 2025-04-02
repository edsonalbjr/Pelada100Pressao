"""
Módulo que contém funções para gerenciar jogadores, como carregar jogadores,
separar por posição e mostrar estatísticas.
"""

import os
import pandas as pd
from typing import List, Dict, Any, Tuple
from modulos.configuracoes import POSICOES

def carregar_jogadores(arquivo_excel: str = "bancodedados.xlsx") -> List[Dict[str, Any]]:
    """
    Carrega jogadores do arquivo Excel ou usa lista padrão se o arquivo não existir
    """
    # Se o arquivo existir, carrega os dados do Excel
    if os.path.exists(arquivo_excel):
        try:
            df = pd.read_excel(arquivo_excel)
            jogadores = []
            
            for _, row in df.iterrows():
                jogador = {
                    'nome': row['jogador'],
                    'habilidade': float(row['habilidade']),
                    'posicao_primaria': row['posicao_primaria'].lower(),
                    'posicao_secundaria': row['posicao_secundaria'].lower() if pd.notna(row['posicao_secundaria']) else 'nenhum',
                    'adm': row['diretor'].lower() == 'sim' if pd.notna(row['diretor']) else False
                }
                jogadores.append(jogador)
            
            return jogadores
        except Exception as e:
            print(f"Erro ao carregar o arquivo Excel: {e}")
            print("Usando lista padrão de jogadores...")
    
    # Lista padrão de jogadores (mesma da versão anterior)
    return [
    {'nome': 'Betinho', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Bidu', 'habilidade': 3, 'posicao_primaria': 'meia', 'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Bruno Pessoa', 'habilidade': 4.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': True},
    {'nome': 'Dato', 'habilidade': 3.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Diego Rocha', 'habilidade': 4.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Eduardo', 'habilidade': 4, 'posicao_primaria': 'meia', 'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Grimauro', 'habilidade': 2, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Jackson', 'habilidade': 4, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'João Vitor', 'habilidade': 4.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Juninho', 'habilidade': 3, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Kiel', 'habilidade': 4.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': True},
    {'nome': 'Léo A.', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Lucas H.', 'habilidade': 3, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Lucas S.', 'habilidade': 1, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Manga', 'habilidade': 4.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Marcos S.', 'habilidade': 3.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Paulo Thiago', 'habilidade': 3.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'zagueiro', 'adm': False},
    {'nome': 'Rafa Ribeiro', 'habilidade': 3, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Raphael B.', 'habilidade': 3.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Sérgio Falcão', 'habilidade': 2.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Teixa', 'habilidade': 2.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Thayan', 'habilidade': 3.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Thiago Alemão', 'habilidade': 2, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Túlio', 'habilidade': 3, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Victor Chaves', 'habilidade': 3, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Xandinho', 'habilidade': 1, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Flavio Ureia', 'habilidade': 3.5, 'posicao_primaria': 'meia', 'posicao_secundaria': 'atacante', 'adm': False},
    {'nome': 'Renan', 'habilidade': 3.5, 'posicao_primaria': 'atacante', 'posicao_secundaria': 'meia', 'adm': False},
    {'nome': 'Thiago Sultanum', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'nenhum', 'adm': False},
    {'nome': 'Elder', 'habilidade': 3.5, 'posicao_primaria': 'zagueiro', 'posicao_secundaria': 'atacante', 'adm': False},
]


def selecionar_jogadores_presentes(todos_jogadores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Permite ao usuário selecionar quais jogadores estão presentes"""
    print("\n=== SELECIONAR JOGADORES PRESENTES ===")
    jogadores_presentes = []
    
    for jogador in todos_jogadores:
        resposta = input(f"O jogador {jogador['nome']} está presente? (s/n): ").lower()
        if resposta == 's':
            jogadores_presentes.append(jogador)
    
    # Mostra o total de jogadores presentes
    print(f"\nTotal de jogadores presentes: {len(jogadores_presentes)}")
    return jogadores_presentes


def separar_por_posicao(jogadores: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Separa jogadores por posição primária e os ordena por habilidade
    """
    jogadores_por_posicao = {
        'zagueiro': [],
        'meia': [],
        'atacante': []
    }
    
    # Também vamos criar listas para jogadores com posições secundárias
    jogadores_secundarios = {
        'zagueiro': [],
        'meia': [],
        'atacante': []
    }
    
    for jogador in jogadores:
        posicao_primaria = jogador['posicao_primaria']
        posicao_secundaria = jogador['posicao_secundaria']
        
        # Adiciona à lista primária
        if posicao_primaria in jogadores_por_posicao:
            jogadores_por_posicao[posicao_primaria].append(jogador)
        
        # Adiciona à lista secundária, se aplicável
        if posicao_secundaria in jogadores_secundarios and posicao_secundaria != 'nenhum':
            jogadores_secundarios[posicao_secundaria].append(jogador)
    
    # Ordena cada lista por habilidade (decrescente)
    for posicao in jogadores_por_posicao:
        jogadores_por_posicao[posicao].sort(key=lambda x: x['habilidade'], reverse=True)
        jogadores_secundarios[posicao].sort(key=lambda x: x['habilidade'], reverse=True)
    
    # Retorna apenas as posições primárias para manter compatibilidade
    return jogadores_por_posicao


def separar_por_posicao_completo(jogadores: List[Dict[str, Any]]) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, List[Dict[str, Any]]]]:
    """
    Separa jogadores por posição primária e secundária, ordenando por habilidade
    Retorna dois dicionários: um para posições primárias e outro para secundárias
    """
    primarias = {
        'zagueiro': [],
        'meia': [],
        'atacante': []
    }
    
    secundarias = {
        'zagueiro': [],
        'meia': [],
        'atacante': []
    }
    
    for jogador in jogadores:
        posicao_primaria = jogador['posicao_primaria']
        posicao_secundaria = jogador['posicao_secundaria']
        
        # Adiciona à lista primária
        if posicao_primaria in primarias:
            primarias[posicao_primaria].append(jogador)
        
        # Adiciona à lista secundária, se aplicável
        if posicao_secundaria in secundarias and posicao_secundaria != 'nenhum':
            secundarias[posicao_secundaria].append(jogador)
    
    # Ordena cada lista por habilidade (decrescente)
    for posicao in primarias:
        primarias[posicao].sort(key=lambda x: x['habilidade'], reverse=True)
        secundarias[posicao].sort(key=lambda x: x['habilidade'], reverse=True)
    
    return primarias, secundarias


def mostrar_estatisticas(jogadores: List[Dict[str, Any]]) -> None:
    """Exibe estatísticas dos jogadores presentes"""
    jogadores_primarios, jogadores_secundarios = separar_por_posicao_completo(jogadores)
    
    print("\n=== ESTATÍSTICAS DOS JOGADORES PRESENTES ===")
    
    # Mostra jogadores por posição primária
    print("\n=== POSIÇÕES PRIMÁRIAS ===")
    for posicao in POSICOES:
        print(f"\n--- {posicao.upper()} ---")
        for jogador in jogadores_primarios[posicao]:
            estrelas = int(jogador['habilidade']) if jogador['habilidade'].is_integer() else jogador['habilidade']
            pos_sec = f" (Sec: {jogador['posicao_secundaria'].capitalize()})" if jogador['posicao_secundaria'] != 'nenhum' else ""
            print(f"{jogador['nome']} ({estrelas}*){pos_sec}")
    
    # Mostra jogadores por posição secundária
    print("\n=== POSIÇÕES SECUNDÁRIAS ===")
    for posicao in POSICOES:
        print(f"\n--- {posicao.upper()} (secundária) ---")
        for jogador in jogadores_secundarios[posicao]:
            estrelas = int(jogador['habilidade']) if jogador['habilidade'].is_integer() else jogador['habilidade']
            print(f"{jogador['nome']} ({estrelas}*) - Primária: {jogador['posicao_primaria'].capitalize()}")
    
    print("\n--- CONTAGEM DE JOGADORES ---")
    print("POR POSIÇÃO PRIMÁRIA:")
    for posicao in POSICOES:
        print(f"{posicao.capitalize()}: {len(jogadores_primarios[posicao])}")
    
    print("\nPOR POSIÇÃO SECUNDÁRIA:")
    for posicao in POSICOES:
        print(f"{posicao.capitalize()}: {len(jogadores_secundarios[posicao])}")
    
    # Exibe estatísticas de habilidade
    habilidades = [j['habilidade'] for j in jogadores]
    media_habilidade = sum(habilidades) / len(habilidades) if habilidades else 0
    
    print(f"\nMédia de habilidade: {media_habilidade:.2f}*")
    print(f"Maior habilidade: {max(habilidades) if habilidades else 0}*")
    print(f"Menor habilidade: {min(habilidades) if habilidades else 0}*")
    
    # Exibe quantidade de administradores
    adms = sum(1 for j in jogadores if j['adm'])
    print(f"Administradores presentes: {adms}")
    print("=" * 40) 