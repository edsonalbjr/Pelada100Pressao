function removerTodosEventosDoCalendario() {
    const calendario = CalendarApp.getDefaultCalendar();
    const dataInicial = new Date("2024-01-01"); // Data inicial para buscar eventos (ajuste conforme necessário)
    const dataFinal = new Date("2024-12-31"); // Data final para buscar eventos (ajuste conforme necessário)
  
    // Busca todos os eventos no intervalo de tempo especificado
    const eventos = calendario.getEvents(dataInicial, dataFinal);
  
    // Remove cada evento encontrado com uma pausa entre as chamadas para evitar atingir os limites de cota
    eventos.forEach(evento => {
      try {
        evento.deleteEvent();
        Utilities.sleep(100); // Pausa de 100ms entre as chamadas para evitar excesso de solicitações
      } catch (e) {
        Logger.log(`Erro ao remover o evento: ${e.message}`);
      }
    });
  
    Logger.log(`${eventos.length} eventos foram removidos.`);
  }
  