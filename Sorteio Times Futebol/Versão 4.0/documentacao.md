Documentação da Versão 4.0 do Sorteio de Times
O código da Versão 4.0 realiza o sorteio de times de futebol com base nas habilidades e posições dos jogadores. Abaixo, você encontrará a documentação do código em um formato Markdown, destacando suas principais funcionalidades.

Jogadores
Os jogadores são representados por dicionários, cada um contendo as seguintes informações:

'nome': Nome do jogador.
'habilidade': Nível de habilidade do jogador (varia de 1 a 5).
'posicao_primaria': Posição primária do jogador (zagueiro, meia, atacante, qualquer).
'posicao_secundaria': Posição secundária do jogador (nenhum, meia, atacante).
'adm': Indica se o jogador é administrador (True/False).
Funções Principais
criar_times(jogadores, num_times)
Esta função cria times aleatórios com base nas habilidades e posições dos jogadores. Recebe como entrada a lista de jogadores e o número de times desejado.

Faz uma cópia aleatória da lista de jogadores.
Separa os jogadores em dois grupos: 'adm': True e 'adm': False.
Ordena ambos os grupos por habilidade de forma decrescente.
Inicializa os times como listas vazias.
Distribui jogadores 'adm': True primeiro, buscando equilibrar posições e habilidades.
Distribui jogadores 'adm': False, considerando posições e habilidades.
Retorna a lista de times criados.
exibir_times(times)
Esta função exibe as informações dos times na saída padrão.

Usa um mapeamento para formatar o nome das posições.
Para cada time, exibe habilidade total, posições primárias e secundárias.
Para cada jogador em um time, exibe nome, habilidade e posições.
Funções Auxiliares
count_positions(time, jogador, posicao=None)
Conta a quantidade de jogadores em cada posição, considerando posições primárias e secundárias.

count_primary_positions(time)
Conta a quantidade de jogadores em cada posição primária.

count_secondary_positions(time)
Conta a quantidade de jogadores em cada posição secundária.

Funcionalidades Adicionais
Habilidade Total Formatada: A habilidade total de cada time é formatada para exibir como inteiro se for o caso.

Nomes e Abreviações: Nomes de posições e jogadores são formatados e abreviados para uma exibição mais concisa.

Ordenação de Jogadores: Os jogadores dentro de cada time são ordenados por habilidade, do maior para o menor.

Execução
O código inicia com a definição dos jogadores, seguido pelas funções principais e execução do sorteio e exibição dos times.

Observações
O código possui comentários explicativos para facilitar a compreensão das etapas e lógica implementadas.

A execução do código resulta no sorteio dos times, exibindo informações detalhadas sobre cada time e jogador.