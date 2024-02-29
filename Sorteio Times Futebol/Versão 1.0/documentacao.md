**Documentação - Versão 1.0**

**1. Introdução:**
   O código em Python na versão 1.0 implementa um simulador para a formação de times de futebol. A principal funcionalidade consiste na distribuição equilibrada de jogadores em times, considerando suas habilidades, posições primárias e secundárias.

**2. Estrutura dos Jogadores:**
   A lista `jogadores` contém dicionários, cada um representando um jogador com as seguintes informações:
   - `"nome"`: Nome do jogador.
   - `"habilidade"`: Habilidade do jogador, representada por um valor numérico.
   - `"adm"`: Indica se o jogador é administrador (True ou False).
   - `"posicao_primaria"`: Posição primária do jogador (zagueiro, meia, atacante, etc.).
   - `"posicao_secundaria"`: Posição secundária do jogador ou None se não houver.

**3. Funções Principais:**

   a. **`criar_times(jogadores, num_times)`**
      - **Entrada:** Lista de jogadores (`jogadores`) e número desejado de times (`num_times`).
      - **Saída:** Lista de times, cada time sendo uma lista de jogadores.
      - **Funcionalidade:** Distribui os jogadores nos times de forma equilibrada, considerando habilidades e posições.

   b. **`exibir_times(times)`**
      - **Entrada:** Lista de times (`times`).
      - **Saída:** Impressão na console dos detalhes dos times.
      - **Funcionalidade:** Apresenta informações sobre a habilidade total de cada time e a distribuição de jogadores por posição.

**4. Funções Auxiliares:**

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
   - O código oferece a opção de trocar aleatoriamente os times e os jogadores dentro de cada time, adicionando variação nas combinações formadas.

**7. Conclusão:**
   A versão 1.0 do código fornece uma base sólida para a formação equilibrada de times de futebol, considerando habilidades e posições dos jogadores. Possíveis melhorias e expansões podem ser consideradas em versões futuras.