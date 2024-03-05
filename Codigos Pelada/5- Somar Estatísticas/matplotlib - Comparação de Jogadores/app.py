import numpy as np
import matplotlib.pyplot as plt

# Dados dos jogadores
jogadores = ['Paulo Thiago', 'Lucas Henrique']
estatisticas_paulo = [14.29, 20.95, 35.24, 48.10]
estatisticas_lucas = [23.60, 7.87, 31.46, 56.18]

categorias = ['Gols por Jogo', 'Assistências por Jogo', 'Participações em Gols por Jogo', 
              'Aproveitamento']

# Preparação dos dados
num_categorias = len(categorias)
angulos = np.linspace(0, 2 * np.pi, num_categorias, endpoint=False)

estatisticas_paulo = np.array(estatisticas_paulo)
estatisticas_lucas = np.array(estatisticas_lucas)

# Criação do gráfico de radar
fig, ax = plt.subplots(subplot_kw={'polar': True}, figsize=(8, 6))

# Estilo de linha e preenchimento
line_width = 2
ax.plot(angulos, estatisticas_paulo, label='Paulo Thiago', color='blue', linewidth=line_width)
ax.fill(angulos, estatisticas_paulo, alpha=0.3, color='blue')

ax.plot(angulos, estatisticas_lucas, label='Lucas Henrique', color='orange', linewidth=line_width)
ax.fill(angulos, estatisticas_lucas, alpha=0.3, color='orange')

# Estilo dos marcadores
marker_size = 8
ax.plot(angulos, estatisticas_paulo, 'o', color='blue', markersize=marker_size)
ax.plot(angulos, estatisticas_lucas, 'o', color='orange', markersize=marker_size)

ax.set_xticks(angulos)
ax.set_xticklabels(categorias, fontsize=12)
ax.set_yticks([])
ax.set_title('Comparação de Estatísticas entre Jogadores', fontsize=16)

# Personalização da legenda
ax.legend(loc='upper right', fontsize=10)

# Personalização da grade de fundo
ax.grid(color='gray', alpha=0.3)

plt.show()
