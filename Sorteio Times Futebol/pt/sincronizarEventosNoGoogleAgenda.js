function sincronizarEventosNoGoogleAgenda() {
    const planilha = SpreadsheetApp.getActiveSpreadsheet();
    const meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
    const calendario = CalendarApp.getDefaultCalendar();
    
    // Pega o ano atual para definir o intervalo de datas
    const anoAtual = new Date().getFullYear();
    const dataInicial = new Date(`${anoAtual}-01-01`); // Data inicial para o ano atual
    const dataFinal = new Date(`${anoAtual}-12-31`); // Data final para o ano atual
  
    const eventosNoGoogleAgenda = calendario.getEvents(dataInicial, dataFinal);
    
    // Criar um mapa de eventos existentes para consulta rápida, filtrando pela tag na descrição
    const mapaDeEventos = {};
    eventosNoGoogleAgenda.forEach(evento => {
      // Verifica se a descrição contém as tags "Banda" e "Gênero"
      if (evento.getDescription().includes("Banda:") && evento.getDescription().includes("Gênero:")) {
        const chave = `${evento.getTitle()}_${evento.getStartTime().toISOString()}_${evento.getDescription().split('\n')[0]}`;
        mapaDeEventos[chave] = evento;
      }
    });
  
    const eventosNaPlanilha = [];
  
    // Iterar por todas as abas de meses para capturar os dados
    meses.forEach(mes => {
      const aba = planilha.getSheetByName(mes);
      if (aba) {
        const intervalo = aba.getRange("A2:F"); // Captura os dados de A2 até F (Banda, Data, Gênero, Cachê, Couvert, Observações)
        const dados = intervalo.getValues().filter(linha => linha[0] && linha[1]); // Filtra apenas linhas com Banda e Data
  
        // Adiciona os dados ao array geral
        dados.forEach(([banda, data, genero, cache, couvert, observacoes]) => {
          const dataConvertida = new Date(data);
          if (!isNaN(dataConvertida)) { // Verifica se a data é válida
            const chave = `${banda}_${dataConvertida.toISOString()}_${genero}`;
            eventosNaPlanilha.push(chave);
  
            if (mapaDeEventos[chave]) {
              // Atualizar o evento existente
              const eventoExistente = mapaDeEventos[chave];
              eventoExistente.setTime(dataConvertida, new Date(dataConvertida.getTime() + 2 * 60 * 60 * 1000)); // Atualiza o horário do evento
              let descricaoEvento = `Banda: ${banda}\nGênero: ${genero}`;
              if (observacoes) {
                descricaoEvento += `\nObservação: ${observacoes}`;
              }
              eventoExistente.setDescription(descricaoEvento);
            } else {
              // Cria um novo evento se não existir
              let descricaoEvento = `Banda: ${banda}\nGênero: ${genero}`;
              if (observacoes) {
                descricaoEvento += `\nObservação: ${observacoes}`;
              }
  
              calendario.createEvent(banda, dataConvertida, new Date(dataConvertida.getTime() + 2 * 60 * 60 * 1000)) // Evento com duração padrão de 2 horas
                .setDescription(descricaoEvento) // Inclui as observações apenas se existirem
                .setLocation("Restaurante Mania Caseira - Gravatá") // Define "Restaurante Mania Caseira - Gravatá" como o local do evento
                .setColor("10"); // Define a cor verde "Sálvia"
            }
          }
        });
      }
    });
  
    // Remover eventos de bandas que não estão mais na planilha
    for (let chave in mapaDeEventos) {
      try {
        if (!eventosNaPlanilha.includes(chave)) {
          mapaDeEventos[chave].deleteEvent();
        }
      } catch (e) {
        Logger.log(`Erro ao tentar deletar o evento: ${e.message}`);
      }
    }
  }
  