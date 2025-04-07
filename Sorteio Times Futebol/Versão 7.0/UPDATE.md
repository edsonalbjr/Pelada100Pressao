# Atualizações Planejadas para o Sistema de Sorteio

## 1. Subdivisão de Posições

### Objetivo

Dividir as posições principais em subposições mais específicas, mantendo o limite de 2 jogadores por posição principal.

### Lógica

1. Cada posição principal (ZAGUEIROS, MEIAS, ATACANTES) terá subposições específicas
2. Um jogador não pode ter a mesma subposição que outro jogador no mesmo time
3. A validação deve ser feita tanto para posição primária quanto secundária
4. Se um jogador for movido para outra posição, sua subposição também deve ser validada
5. O sistema deve tentar manter o equilíbrio entre as subposições

### Estrutura Proposta

```python
SUBPOSICOES = {
    'ATACANTES': {
        'centroavante': 'ATACANTES',
        'ponta_direito': 'ATACANTES',
        'ponta_esquerdo': 'ATACANTES',
        'segundo_atacante': 'ATACANTES'
    },
    'MEIAS': {
        'meia': 'MEIAS',
        'volante': 'MEIAS',
        'meia_ligacao': 'MEIAS',
        'meia_atacante': 'MEIAS'
    },
    'ZAGUEIROS': {
        'zagueiro_central': 'ZAGUEIROS',
        'zagueiro_direito': 'ZAGUEIROS',
        'zagueiro_esquerdo': 'ZAGUEIROS',
        'lateral_direito': 'ZAGUEIROS',
        'lateral_esquerdo': 'ZAGUEIROS'
    }
}
```

### Implementação

1. Modificar a estrutura de dados dos jogadores:

```python
jogador = {
    'nome': 'Nome',
    'habilidade': 5.0,
    'posicao_primaria': 'centroavante',
    'posicao_secundaria': 'ponta_direito',
    'subposicao_primaria': 'centroavante',
    'subposicao_secundaria': 'ponta_direito'
}
```

2. Adicionar validação na redistribuição:

```python
def validar_subposicoes(time, posicao):
    """Verifica se há jogadores com a mesma subposição"""
    subposicoes = [j['subposicao_primaria'] for j in time[posicao]]
    return len(subposicoes) == len(set(subposicoes))
```

## 2. Atributos Físicos

### Objetivo

Adicionar atributos físicos para evitar times desequilibrados em velocidade/peso.

### Lógica

1. Cada jogador terá atributos físicos (velocidade, peso, altura)
2. O sistema calculará a média de cada atributo por time
3. Ao distribuir jogadores, o sistema verificará:
   - Se a velocidade média do time não ficará muito baixa
   - Se o peso médio do time não ficará muito alto
   - Se há equilíbrio entre jogadores rápidos e lentos
4. A distribuição priorizará times com atributos físicos equilibrados
5. Se necessário, o sistema poderá trocar jogadores entre times para melhorar o equilíbrio físico

### Estrutura Proposta

```python
jogador = {
    'nome': 'Nome',
    'habilidade': 5.0,
    'velocidade': 3,  # 1 a 5
    'peso': 75,      # em kg
    'altura': 1.80   # em metros
}
```

### Implementação

1. Adicionar função para calcular equilíbrio físico:

```python
def calcular_equilibrio_fisico(time):
    """Calcula o equilíbrio físico do time"""
    velocidade_media = sum(j['velocidade'] for j in time) / len(time)
    peso_medio = sum(j['peso'] for j in time) / len(time)
    return {
        'velocidade': velocidade_media,
        'peso': peso_medio
    }
```

2. Modificar a função de distribuição para considerar o equilíbrio físico:

```python
def encontrar_melhor_dupla(jogadores, valor_ideal, time_atual):
    """Encontra a melhor dupla considerando equilíbrio físico"""
    melhor_dupla = None
    menor_diferenca = float('inf')

    for dupla in combinations(jogadores, 2):
        # Verificar equilíbrio físico
        if verificar_equilibrio_fisico(dupla, time_atual):
            soma = sum(j['habilidade'] for j in dupla)
            diferenca = abs(soma - valor_ideal)
            if diferenca < menor_diferenca:
                menor_diferenca = diferenca
                melhor_dupla = dupla

    return melhor_dupla
```

## 3. Histórico de Times

### Objetivo

Manter histórico para evitar que jogadores fiquem sempre no mesmo time.

### Lógica

1. O sistema manterá um histórico dos últimos 5 times de cada jogador
2. Ao distribuir jogadores, o sistema verificará:
   - Se o jogador já esteve no time nos últimos 5 sorteios
   - A frequência geral do jogador em cada time
   - Se há times que o jogador nunca ou raramente jogou
3. Prioridades na distribuição:
   - Evitar times onde o jogador esteve recentemente
   - Preferir times onde o jogador jogou menos vezes
   - Garantir que todos os times tenham chance de receber o jogador
4. O histórico será salvo e atualizado após cada sorteio
5. O sistema terá uma opção para visualizar e resetar o histórico

### Estrutura Proposta

```python
historico = {
    'jogador_id': {
        'ultimos_times': [1, 3, 2, 1, 4],  # últimos 5 times
        'frequencia_times': {1: 5, 2: 3, 3: 4, 4: 2, 5: 1}  # contagem por time
    }
}
```

### Implementação

1. Adicionar função para verificar histórico:

```python
def verificar_historico(jogador, time_num):
    """Verifica se o jogador pode ir para o time baseado no histórico"""
    if time_num in jogador['historico']['ultimos_times']:
        return False
    if jogador['historico']['frequencia_times'][time_num] > media_geral:
        return False
    return True
```

2. Modificar a distribuição para considerar o histórico:

```python
def distribuir_jogadores_com_historico(jogadores, times):
    """Distribui jogadores considerando histórico"""
    for jogador in jogadores:
        times_disponiveis = [t for t in times if verificar_historico(jogador, t)]
        if times_disponiveis:
            time_escolhido = escolher_time_menos_frequente(times_disponiveis, jogador)
            times[time_escolhido].append(jogador)
            atualizar_historico(jogador, time_escolhido)
```

## 4. Distribuição Equilibrada de Números

### Objetivo

Evitar que jogadores fiquem sempre no mesmo número de time.

### Lógica

1. O sistema manterá um registro das últimas posições de cada jogador
2. Ao distribuir jogadores, o sistema verificará:
   - As últimas 5 posições do jogador
   - A frequência do jogador em cada posição
   - Se há posições que o jogador nunca ou raramente ocupou
3. Prioridades na distribuição:
   - Evitar posições recentes do jogador
   - Preferir posições menos frequentes
   - Garantir que todas as posições tenham chance
4. Se um jogador estiver sempre na mesma posição:
   - O sistema tentará trocar com outro jogador
   - Considerará o histórico de ambos os jogadores
   - Manterá o equilíbrio de habilidades
5. O sistema mostrará estatísticas de distribuição por posição

### Implementação

1. Adicionar contagem de posições:

```python
contagem_posicoes = {
    'jogador_id': {
        'ultimas_posicoes': [1, 2, 3, 4, 5],
        'frequencia_posicoes': {1: 3, 2: 2, 3: 4, 4: 1, 5: 5}
    }
}
```

2. Modificar a função de distribuição:

```python
def distribuir_equilibrado(jogadores, times):
    """Distribui jogadores equilibrando as posições"""
    for jogador in jogadores:
        posicoes_disponiveis = [p for p in range(1, 6)
                              if p not in jogador['contagem_posicoes']['ultimas_posicoes']]
        if posicoes_disponiveis:
            posicao_escolhida = escolher_posicao_menos_frequente(posicoes_disponiveis, jogador)
            times[posicao_escolhida].append(jogador)
            atualizar_contagem_posicoes(jogador, posicao_escolhida)
```

## Considerações de Implementação

1. **Ordem de Prioridade**:

   - Primeiro implementar subposições
   - Depois atributos físicos
   - Em seguida histórico de times
   - Por último distribuição equilibrada de números

2. **Impacto no Desempenho**:

   - Adicionar cache para cálculos frequentes
   - Otimizar verificações de histórico
   - Considerar paralelização para cálculos pesados

3. **Persistência de Dados**:

   - Salvar histórico em arquivo JSON
   - Implementar backup automático
   - Adicionar opção para resetar histórico

4. **Interface do Usuário**:
   - Adicionar visualização de histórico
   - Mostrar estatísticas de distribuição
   - Permitir configuração de pesos para cada critério
