function alterarCoresDasAbasEOcultarMesesPassados() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet();
    var today = new Date();
    var currentMonth = today.getMonth(); // Retorna o mês atual (0 = Janeiro, 11 = Dezembro)
    
    var monthSheets = {
      0: "Janeiro",
      1: "Fevereiro",
      2: "Março",
      3: "Abril",
      4: "Maio",
      5: "Junho",
      6: "Julho",
      7: "Agosto",
      8: "Setembro",
      9: "Outubro",
      10: "Novembro",
      11: "Dezembro"
    };
  
    for (var i = 0; i < 12; i++) {
      var sheetName = monthSheets[i];
      var sh = sheet.getSheetByName(sheetName);
  
      if (sh) {
        if (i < currentMonth) {
          // Mês passado: vermelho e ocultar
          sh.setTabColor("ff0000");
          sh.hideSheet();
        } else if (i == currentMonth) {
          // Mês atual: verde e garantir que esteja visível
          sh.setTabColor("0B8043");
          sh.showSheet();
        } else {
          // Próximos meses: laranja e garantir que estejam visíveis
          sh.setTabColor("ffa500");
          sh.showSheet();
        }
      }
    }
  }
  