# Sistema de Sorteio de Times de Futebol

## 📋 Descrição

Sistema desenvolvido para distribuir jogadores em times de futebol de forma equilibrada, considerando suas habilidades e posições. O sistema garante que os times sejam montados de forma justa, mantendo um equilíbrio entre as posições e as habilidades dos jogadores.

## 🎯 Objetivo

- Distribuir jogadores em 5 times
- Manter equilíbrio de habilidades entre os times
- Respeitar as posições dos jogadores (Zagueiros, Meias e Atacantes)
- Garantir que cada time tenha jogadores suficientes em cada posição
- Embaralhar a ordem dos times para maior aleatoriedade

## 🧩 Estrutura do Sistema

### 1. Posições

O sistema trabalha com 3 posições principais:

- ZAGUEIROS
- MEIAS
- ATACANTES

### 2. Dados dos Jogadores

Cada jogador possui:

- Nome
- Habilidade (nota de 1 a 5)
- Posição Primária
- Posição Secundária (pode ser 'nenhum')

### 3. Processo de Distribuição

#### 3.1. Distribuição Inicial

- Os jogadores são inicialmente agrupados por sua posição primária
- Cada posição é ordenada por habilidade (do maior para o menor)

#### 3.2. Redistribuição de Jogadores

O sistema tenta equilibrar o número de jogadores em cada posição seguindo esta ordem:

1. **Uso de Posições Secundárias**

   - Verifica se há jogadores com posição secundária adequada
   - Move jogadores mantendo a ordem de habilidade

2. **Uso de Coringas**
   - Se não houver jogadores com posição secundária adequada
   - Seleciona o jogador com maior habilidade disponível
   - Move este jogador para a posição necessária

#### 3.3. Cálculo de Equilíbrio

- Calcula a soma total de habilidades
- Define meta de habilidades por posição (total/3)
- Define meta de habilidades por time (total/5)

#### 3.4. Montagem dos Times

- Distribui jogadores para os 5 times
- Garante que cada time tenha jogadores em todas as posições
- Tenta manter o equilíbrio de habilidades entre os times
- Embaralha a ordem dos times para maior aleatoriedade

## 📊 Saída do Sistema

O sistema gera as seguintes informações:

1. **Lista Inicial de Jogadores**

   - Mostra jogadores agrupados por posição inicial

2. **Análise de Distribuição**

   - Mostra quantidade de jogadores em cada posição
   - Antes e depois da redistribuição

3. **Soma das Notas**

   - Total de pontos
   - Meta por posição
   - Meta por time
   - Diferença em relação à meta

4. **Times Montados**
   - Lista completa de cada time
   - Jogadores por posição
   - Total de habilidades do time
   - Ordem dos times embaralhada aleatoriamente

## 🔄 Lógica de Redistribuição

### Prioridades

1. Manter jogadores em suas posições primárias
2. Usar posições secundárias quando necessário
3. Usar coringas (melhores jogadores) como última opção

### Regras

- Cada posição deve ter 10 jogadores
- Movimentos são feitos mantendo a ordem de habilidade
- Coringas são escolhidos entre os jogadores de maior habilidade
- O sistema para quando todas as posições têm 10 jogadores
- A ordem final dos times é sempre embaralhada aleatoriamente

## 📝 Exemplo de Uso

1. Definir lista de jogadores com:

   - Nome
   - Habilidade
   - Posição Primária
   - Posição Secundária

2. Executar o sistema
3. Analisar a distribuição gerada
4. Verificar o equilíbrio dos times
5. Observar a ordem aleatória dos times

## ⚙️ Requisitos

- Python 3.x
- Bibliotecas:
  - itertools
  - copy
  - random

## 🚀 Como Executar

1. Certifique-se de ter a lista de jogadores definida
2. Execute o script `sorteio_posicoes.py`
3. Analise a saída gerada
4. Observe a ordem aleatória dos times

## 📈 Considerações

- O sistema prioriza o equilíbrio de habilidades
- Jogadores podem ser movidos para posições diferentes se necessário
- A redistribuição é feita de forma inteligente para manter o equilíbrio
- O uso de coringas é uma última opção para garantir a completude dos times
- A ordem dos times é sempre embaralhada para maior aleatoriedade
