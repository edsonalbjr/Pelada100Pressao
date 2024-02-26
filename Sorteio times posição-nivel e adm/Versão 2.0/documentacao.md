**Documentação - Versão 2.0**

**1. Introdução:**
   A versão 2.0 do código em Python aprimora o simulador de formação de times de futebol introduzindo novas funcionalidades. A principal adição é a inclusão da posição "Qualquer", proporcionando maior flexibilidade na alocação de jogadores em diferentes posições.

**2. Novas Funcionalidades e Alterações:**

   a. **Adição da Posição "Qualquer":**
      - Uma nova posição chamada "Qualquer" foi introduzida para jogadores cuja posição primária pode ser alocada em qualquer posição no time.

   b. **Lógica Aprimorada na Distribuição:**
      - Jogadores com "adm": False e posição primária como "Qualquer" são alocados no time com menor habilidade, adicionando uma nova estratégia de formação.

   c. **Atualização na Lógica de Remoção de Jogadores:**
      - Jogadores com posição primária como "Qualquer" só são removidos da lista geral se essa posição não for "Qualquer", evitando remoção antes da distribuição.

   d. **Adição de Condição "Qualquer" na Impressão:**
      - Na função `exibir_times`, as condições de impressão para posições primárias e secundárias foram atualizadas para filtrar apenas as posições com valores não zerados, proporcionando uma saída mais limpa.

**3. Funções Principais (Mantidas):**

   a. **`criar_times(jogadores, num_times)`**
      - **Entrada:** Lista de jogadores (`jogadores`) e número desejado de times (`num_times`).
      - **Saída:** Lista de times, cada time sendo uma lista de jogadores.
      - **Funcionalidade:** Distribui os jogadores nos times de forma equilibrada, considerando habilidades e posições.

   b. **`exibir_times(times)`**
      - **Entrada:** Lista de times (`times`).
      - **Saída:** Impressão na console dos detalhes dos times.
      - **Funcionalidade:** Apresenta informações sobre a habilidade total de cada time e a distribuição de jogadores por posição.

**4. Funções Auxiliares (Mantidas):**

   a. **`count_positions(time, jogador)`**
      - **Entrada:** Time (`time`) e jogador (`jogador`).
      - **Saída:** Número de jogadores em posições primárias e secundárias.
      - **Funcionalidade:** Conta a quantidade de jogadores em cada posição do time.

   b. **`count_primary_positions(time)`**
      - **Entrada:** Time (`time`).
      - **Saída:** Dicionário com contagem de jogadores por posição primária.
      - **Funcionalidade:** Conta a quantidade de jogadores em cada posição primária no time.

   c. **`count_secondary_positions(time)`**
      - **Entrada:** Time (`time`).
      - **Saída:** Dicionário com contagem de jogadores por posição secundária.
      - **Funcionalidade:** Conta a quantidade de jogadores em cada posição secundária no time.

**5. Execução do Código:**
   - Defina o número de times (`num_times`) e o número máximo de jogadores por time (`max_jogadores_por_time`).
   - Chame a função `criar_times(jogadores, num_times)` para criar os times.
   - Chame a função `exibir_times(times)` para exibir os detalhes dos times inicialmente ou após trocas aleatórias.

**6. Observações:**
   - A versão 2.0 oferece maior flexibilidade na formação de times, especialmente com a adição da posição "Qualquer", permitindo uma distribuição mais dinâmica dos jogadores.