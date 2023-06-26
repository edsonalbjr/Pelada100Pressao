function adicionarLance() {
  var jogo = document.getElementById("jogo").value;
  var jogador = document.getElementById("jogador").value;
  var tipoLance = document.getElementById("tipoLance").value;
  var comecoLance = document.getElementById("comecoLance").value;
  var finalLance = document.getElementById("finalLance").value;

  var tabela = document
    .getElementById("tabelaLances")
    .getElementsByTagName("tbody")[0];
  var novaLinha = tabela.insertRow(tabela.rows.length);

  var colunaJogo = novaLinha.insertCell(0);
  colunaJogo.innerHTML = jogo;

  var colunajogador = novaLinha.insertCell(1);
  colunajogador.innerHTML = jogador;

  var colunaTipoLance = novaLinha.insertCell(2);
  colunaTipoLance.innerHTML = tipoLance;

  var colunaComecoLance = novaLinha.insertCell(3);
  colunaComecoLance.innerHTML = comecoLance;

  var colunaFinalLance = novaLinha.insertCell(4);
  colunaFinalLance.innerHTML = finalLance;

  // Limpar os campos de entrada após adicionar o lance à tabela
  document.getElementById("comecoLance").value = "";
  document.getElementById("finalLance").value = "";
}

function exportarParaExcel() {
  var workbook = XLSX.utils.book_new();

  var lancesWorksheetData = [
    [
      "Jogo",
      "Jogador",
      "Tipo do Lance",
      "Começo do Lance",
      "Final do Lance",
    ],
  ];
  var tabela = document.getElementById("tabelaLances");
  var linhas = tabela.getElementsByTagName("tr");

  for (var i = 1; i < linhas.length; i++) {
    var linha = linhas[i];
    var jogo = linha.cells[0].innerText;
    var jogador = linha.cells[1].innerText;
    var tipoLance = linha.cells[2].innerText;
    var comecoLance = linha.cells[3].innerText;
    var finalLance = linha.cells[4].innerText;

    lancesWorksheetData.push([
      jogo,
      jogador,
      tipoLance,
      comecoLance,
      finalLance,
    ]);
  }

  var lancesWorksheet = XLSX.utils.aoa_to_sheet(lancesWorksheetData);
  XLSX.utils.book_append_sheet(
    workbook,
    lancesWorksheet,
    "Melhores Momentos"
  );

  var wbout = XLSX.write(workbook, { bookType: "xlsx", type: "binary" });
  saveWorkbook(wbout, "melhores-momentos.xlsx");
}

function saveWorkbook(workbookOutput, fileName) {
  var blob = new Blob([s2ab(workbookOutput)], {
    type: "application/octet-stream",
  });
  var downloadLink = document.createElement("a");
  downloadLink.href = URL.createObjectURL(blob);
  downloadLink.download = fileName;
  downloadLink.click();
  URL.revokeObjectURL(downloadLink.href);
}

function s2ab(s) {
  var buf = new ArrayBuffer(s.length);
  var view = new Uint8Array(buf);
  for (var i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xff;
  return buf;
}