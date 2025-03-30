# Documentação do Sistema de Sorteio de Times

## Visão Geral

O sistema foi desenvolvido para realizar o sorteio equilibrado de 5 times de futebol, considerando as posições dos jogadores (zagueiro, meia e atacante) e suas habilidades (notas de 1 a 5 estrelas).

## Lógica do Sorteio

### 1. Carregamento e Organização Inicial

- Carrega jogadores do banco de dados
- Organiza jogadores em 3 grupos por posição primária:
  - Zagueiros
  - Meias
  - Atacantes
- Cada posição deve ter idealmente 10 jogadores (2 por time)

### 2. Balanceamento de Posições

Se alguma posição não tiver exatamente 10 jogadores, o sistema:

1. Identifica posições com excesso e falta de jogadores
2. Move jogadores entre posições usando posições secundárias
3. Prioriza mover jogadores que têm posição secundária compatível
4. Casos especiais tratados:
   - Falta zagueiro (9) e sobra atacante (11)
   - Falta meia (9) e sobra atacante (11)
   - Falta zagueiro (9) e sobra meia (11)

### 3. Distribuição dos Jogadores nos Times

#### 3.1 Identificação de Jogadores Fracos

- Jogadores fracos são aqueles com nota < 3 estrelas
- Sistema identifica todos os jogadores fracos em cada posição

#### 3.2 Distribuição dos Jogadores Fracos

1. Para cada posição (zagueiros, meias, atacantes):
   - Identifica jogadores com nota < 3
   - Tenta distribuir cada jogador fraco em um time diferente
   - Se não for possível (mais jogadores fracos que times), avisa que um time terá mais de um jogador fraco

#### 3.3 Distribuição dos Demais Jogadores

1. Ordena jogadores restantes por habilidade (do maior para o menor)
2. Para cada posição:
   - Distribui jogadores nos times que ainda precisam completar a posição
   - Considera a soma total de habilidades do time para manter o equilíbrio
   - Cada time deve receber 2 jogadores por posição

### 4. Embaralhamento Final

- Após a distribuição completa, os números dos times são embaralhados
- Time 1 pode se tornar Time 2, 3, 4 ou 5 aleatoriamente
- Garante que o número do time seja imprevisível

## Regras e Restrições

### Jogadores por Time

- Cada time deve ter 6 jogadores:
  - 2 zagueiros
  - 2 meias
  - 2 atacantes

### Balanceamento de Habilidades

- Sistema tenta manter a soma total de estrelas equilibrada entre os times
- Jogadores fracos (< 3 estrelas) são distribuídos em times diferentes
- Não há priorização especial para times que receberam jogadores fracos

### Posições Secundárias

- Jogadores podem ter uma posição secundária
- Usadas principalmente no balanceamento inicial de posições
- Ajuda a resolver problemas de distribuição desigual de jogadores

## Exemplo de Saída

```
--- Time X ---
ZAGUEIROS
1- Jogador A            4.5        Zagueiro             -
2- Jogador B            3.0        Zagueiro             Meia

MEIAS
1- Jogador C            5.0        Meia                 Atacante
2- Jogador D            3.5        Meia                 -

ATACANTES
1- Jogador E            4.0        Atacante             -
2- Jogador F            3.0        Atacante             Meia

Total de estrelas: 23.0
```

## Observações Importantes

1. O sistema prioriza distribuir jogadores fracos em times diferentes
2. A soma total de estrelas entre os times tende a ficar equilibrada
3. Os números dos times são sorteados aleatoriamente ao final
4. Posições secundárias são consideradas para balanceamento
5. O sistema avisa quando não consegue evitar times com múltiplos jogadores fracos
