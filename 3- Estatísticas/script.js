window.addEventListener("DOMContentLoaded", function () {
  preencherTabelaGoleiros();
  preencherTabela("time1", "Time 1");
  preencherTabela("time2", "Time 2");
  preencherTabela("time3", "Time 3");
  preencherTabela("time4", "Time 4");
  preencherTabela("time5", "Time 5");
});

function preencherTabelaGoleiros() {
  var tableBody = document.getElementById("goleiros-table");

  for (var i = 0; i < goleiros.length; i++) {
    var tr = document.createElement("tr");

    var tdNome = document.createElement("td");
    tdNome.textContent = goleiros[i].nome;
    tr.appendChild(tdNome);

    var tdGol = criarCelulaEstatistica(goleiros[i], "gol");
    tr.appendChild(tdGol);

    var tdFinalizacaoTrave = criarCelulaEstatistica(
      goleiros[i],
      "finalizacaoTrave"
    );
    tr.appendChild(tdFinalizacaoTrave);

    var tdFinalizacaoDefendida = criarCelulaEstatistica(
      goleiros[i],
      "finalizacaoDefendida"
    );
    tr.appendChild(tdFinalizacaoDefendida);

    var tdFinalizacaoFora = criarCelulaEstatistica(
      goleiros[i],
      "finalizacaoFora"
    );
    tr.appendChild(tdFinalizacaoFora);

    var tdAssistencia = criarCelulaEstatistica(
      goleiros[i],
      "assistencia"
    );
    tr.appendChild(tdAssistencia);

    var tdLancamentoLongo = criarCelulaEstatistica(
      goleiros[i],
      "lancamentoLongo"
    );
    tr.appendChild(tdLancamentoLongo);

    var tdDesarme = criarCelulaEstatistica(goleiros[i], "desarme");
    tr.appendChild(tdDesarme);

    var tdFaltaSofrida = criarCelulaEstatistica(
      goleiros[i],
      "faltaSofrida"
    );
    tr.appendChild(tdFaltaSofrida);

    var tdPenaltiSofrido = criarCelulaEstatistica(
      goleiros[i],
      "penaltiSofrido"
    );
    tr.appendChild(tdPenaltiSofrido);

    var tdJogoSemSofrerGol = criarCelulaEstatistica(
      goleiros[i],
      "jogoSemSofrerGol"
    );
    tr.appendChild(tdJogoSemSofrerGol);

    var tdDefesa = criarCelulaEstatistica(goleiros[i], "defesa");
    tr.appendChild(tdDefesa);

    var tdDefesaPenalti = criarCelulaEstatistica(
      goleiros[i],
      "defesaPenalti"
    );
    tr.appendChild(tdDefesaPenalti);

    var tdGolSofrido = criarCelulaEstatistica(goleiros[i], "golSofrido");
    tr.appendChild(tdGolSofrido);

    var tdFaltaCometida = criarCelulaEstatistica(
      goleiros[i],
      "faltaCometida"
    );
    tr.appendChild(tdFaltaCometida);

    var tdGolContra = criarCelulaEstatistica(goleiros[i], "golContra");
    tr.appendChild(tdGolContra);

    var tdCartaoAmarelo = criarCelulaEstatistica(
      goleiros[i],
      "cartaoAmarelo"
    );
    tr.appendChild(tdCartaoAmarelo);

    var tdCartaoVermelho = criarCelulaEstatistica(
      goleiros[i],
      "cartaoVermelho"
    );
    tr.appendChild(tdCartaoVermelho);

    var tdPenaltiPerdido = criarCelulaEstatistica(
      goleiros[i],
      "penaltiPerdido"
    );
    tr.appendChild(tdPenaltiPerdido);

    var tdPenaltiCometido = criarCelulaEstatistica(
      goleiros[i],
      "penaltiCometido"
    );
    tr.appendChild(tdPenaltiCometido);

    tableBody.appendChild(tr);
  }
}

function preencherTabela(timeId, titulo) {
  var tableBody = document.getElementById(timeId);

  for (var i = 0; i < 5; i++) {
    var tr = document.createElement("tr");

    var tdNome = document.createElement("td");
    var select = criarSelectJogadores();
    tdNome.appendChild(select);
    tr.appendChild(tdNome);

    var jogador = {
      nome: "",
      gol: 0,
      finalizacaoTrave: 0,
      finalizacaoDefendida: 0,
      finalizacaoFora: 0,
      assistencia: 0,
      lancamentoLongo: 0,
      desarme: 0,
      faltaSofrida: 0,
      penaltiSofrido: 0,
      jogoSemSofrerGol: 0,
      defesa: 0,
      defesaPenalti: 0,
      golSofrido: 0,
      faltaCometida: 0,
      golContra: 0,
      cartaoAmarelo: 0,
      cartaoVermelho: 0,
      penaltiPerdido: 0,
      penaltiCometido: 0,
    };
    jogador.nome = select.value;
    jogadores.push(jogador);

    var tdGol = criarCelulaEstatistica(jogador, "gol");
    tr.appendChild(tdGol);

    var tdFinalizacaoTrave = criarCelulaEstatistica(
      jogador,
      "finalizacaoTrave"
    );
    tr.appendChild(tdFinalizacaoTrave);

    var tdFinalizacaoDefendida = criarCelulaEstatistica(
      jogador,
      "finalizacaoDefendida"
    );
    tr.appendChild(tdFinalizacaoDefendida);

    var tdFinalizacaoFora = criarCelulaEstatistica(
      jogador,
      "finalizacaoFora"
    );
    tr.appendChild(tdFinalizacaoFora);

    var tdAssistencia = criarCelulaEstatistica(jogador, "assistencia");
    tr.appendChild(tdAssistencia);

    var tdLancamentoLongo = criarCelulaEstatistica(
      jogador,
      "lancamentoLongo"
    );
    tr.appendChild(tdLancamentoLongo);

    var tdDesarme = criarCelulaEstatistica(jogador, "desarme");
    tr.appendChild(tdDesarme);

    var tdFaltaSofrida = criarCelulaEstatistica(jogador, "faltaSofrida");
    tr.appendChild(tdFaltaSofrida);

    var tdPenaltiSofrido = criarCelulaEstatistica(
      jogador,
      "penaltiSofrido"
    );
    tr.appendChild(tdPenaltiSofrido);

    var tdJogoSemSofrerGol = criarCelulaEstatistica(
      jogador,
      "jogoSemSofrerGol"
    );
    tr.appendChild(tdJogoSemSofrerGol);

    var tdDefesa = criarCelulaEstatistica(jogador, "defesa");
    tr.appendChild(tdDefesa);

    var tdDefesaPenalti = criarCelulaEstatistica(
      jogador,
      "defesaPenalti"
    );
    tr.appendChild(tdDefesaPenalti);

    var tdGolSofrido = criarCelulaEstatistica(jogador, "golSofrido");
    tr.appendChild(tdGolSofrido);

    var tdFaltaCometida = criarCelulaEstatistica(
      jogador,
      "faltaCometida"
    );
    tr.appendChild(tdFaltaCometida);

    var tdGolContra = criarCelulaEstatistica(jogador, "golContra");
    tr.appendChild(tdGolContra);

    var tdCartaoAmarelo = criarCelulaEstatistica(
      jogador,
      "cartaoAmarelo"
    );
    tr.appendChild(tdCartaoAmarelo);

    var tdCartaoVermelho = criarCelulaEstatistica(
      jogador,
      "cartaoVermelho"
    );
    tr.appendChild(tdCartaoVermelho);

    var tdPenaltiPerdido = criarCelulaEstatistica(
      jogador,
      "penaltiPerdido"
    );
    tr.appendChild(tdPenaltiPerdido);

    var tdPenaltiCometido = criarCelulaEstatistica(
      jogador,
      "penaltiCometido"
    );
    tr.appendChild(tdPenaltiCometido);

    tableBody.appendChild(tr);
  }
}

function criarSelectJogadores() {
  var select = document.createElement("select");

  var optgroupMensalistas = document.createElement("optgroup");
  optgroupMensalistas.label = "Mensalistas";
  var mensalistas = [
    " ",
    "Albert",
    "Betinho",
    "Bruno Pessoa",
    "Diego Rocha",
    "Eduardo",
    "Eric",
    "Flávio",
    "Henrique Silva",
    "Jorge",
    "Kiel",
    "Lucas Henrique",
    "Lucas Silveira",
    "Manga",
    "Marcelinho",
    "Marquinhos S.",
    "Matheus Ureia",
    "Niclaudio",
    "Paulo Thiago",
    "Raphael Borges",
    "Teixa",
    "Tiago Alemão",
    "Victor Assis",
    "Victor Cabeça",
    "Vinícius",
    "Vitor Salgado",
  ];
  for (var i = 0; i < mensalistas.length; i++) {
    var option = document.createElement("option");
    option.value = mensalistas[i];
    option.textContent = mensalistas[i];
    optgroupMensalistas.appendChild(option);
  }
  select.appendChild(optgroupMensalistas);

  var optgroupDiaristas = document.createElement("optgroup");
  optgroupDiaristas.label = "Diaristas";
  var diaristas = [
    "Balbino",
    "Bidu",
    "Dato",
    "Edmundo",
    "Elvinho",
    "Felipe Melo",
    "Gabriel Ferreira",
    "Gil",
    "Ícaro",
    "Ítalo",
    "Jackson",
    "Jefferson",
    "Juninho",
    "Pou",
    "Renan",
    "Ronaldinho",
    "Teteca",
    "Winnicius C.",
    "Alysson Pink",
    "Vinicinho",
    "Lázaro",
    "Pedro",
    "Emerson",
  ];
  for (var i = 0; i < diaristas.length; i++) {
    var option = document.createElement("option");
    option.value = diaristas[i];
    option.textContent = diaristas[i];
    optgroupDiaristas.appendChild(option);
  }
  select.appendChild(optgroupDiaristas);

  return select;
}

function criarCelulaEstatistica(jogador, estatistica) {
  var td = document.createElement("td");

  var minusButton = document.createElement("button");
  minusButton.textContent = "-1";
  minusButton.addEventListener("click", function () {
    decrementar(jogador, estatistica, td);
  });

  var valueSpan = document.createElement("span");
  valueSpan.textContent = jogador[estatistica];

  var plusButton = document.createElement("button");
  plusButton.textContent = "+1";
  plusButton.addEventListener("click", function () {
    incrementar(jogador, estatistica, td);
  });

  td.appendChild(minusButton);
  td.appendChild(document.createTextNode(" "));
  td.appendChild(valueSpan);
  td.appendChild(document.createTextNode(" "));
  td.appendChild(plusButton);

  return td;
}

function incrementar(jogador, estatistica, td) {
  jogador[estatistica] += 1;
  td.querySelector("span").textContent = jogador[estatistica];
}

function decrementar(jogador, estatistica, td) {
  if (jogador[estatistica] > 0) {
    jogador[estatistica] -= 1;
    td.querySelector("span").textContent = jogador[estatistica];
  }
}

function exportToExcel() {
  var workbook = XLSX.utils.book_new();

  var goleirosWorksheetData = [
    [
      "Goleiros",
      "Gols",
      "Finalização na Trave",
      "Finalização Defendida",
      "Finalização para Fora",
      "Assistência",
      "Lançamento Longo",
      "Desarme",
      "Falta Sofrida",
      "Pênalti Sofrido",
      "Jogo sem Sofrer Gol",
      "Defesa",
      "Defesa de Pênalti",
      "Gol Sofrido",
      "Falta Cometida",
      "Gol Contra",
      "Cartão Amarelo",
      "Cartão Vermelho",
      "Pênalti Perdido",
      "Pênalti Cometido",
    ],
  ];
  for (var i = 0; i < goleiros.length; i++) {
    var goleiro = goleiros[i];
    goleirosWorksheetData.push([
      goleiro.nome,
      goleiro.gol,
      goleiro.finalizacaoTrave,
      goleiro.finalizacaoDefendida,
      goleiro.finalizacaoFora,
      goleiro.assistencia,
      goleiro.lancamentoLongo,
      goleiro.desarme,
      goleiro.faltaSofrida,
      goleiro.penaltiSofrido,
      goleiro.jogoSemSofrerGol,
      goleiro.defesa,
      goleiro.defesaPenalti,
      goleiro.golSofrido,
      goleiro.faltaCometida,
      goleiro.golContra,
      goleiro.cartaoAmarelo,
      goleiro.cartaoVermelho,
      goleiro.penaltiPerdido,
      goleiro.penaltiCometido,
    ]);
  }
  var goleirosWorksheet = XLSX.utils.aoa_to_sheet(goleirosWorksheetData);
  XLSX.utils.book_append_sheet(workbook, goleirosWorksheet, "Goleiros");

  var times = ["time1", "time2", "time3", "time4", "time5"];
  times.forEach(function (time) {
    var timeTable = document.getElementById(time);
    var timeRows = timeTable.getElementsByTagName("tr");
    var timeWorksheetData = getTableData(timeRows);
    timeWorksheetData.unshift([
      "Jogadores",
      "Gols",
      "Finalização na Trave",
      "Finalização Defendida",
      "Finalização para Fora",
      "Assistência",
      "Lançamento Longo",
      "Desarme",
      "Falta Sofrida",
      "Pênalti Sofrido",
      "Jogo sem Sofrer Gol",
      "Defesa",
      "Defesa de Pênalti",
      "Gol Sofrido",
      "Falta Cometida",
      "Gol Contra",
      "Cartão Amarelo",
      "Cartão Vermelho",
      "Pênalti Perdido",
      "Pênalti Cometido",
    ]); // Adiciona os títulos na primeira linha
    var timeWorksheet = XLSX.utils.aoa_to_sheet(timeWorksheetData);
    XLSX.utils.book_append_sheet(workbook, timeWorksheet, time);
  });

  var wbout = XLSX.write(workbook, { bookType: "xlsx", type: "binary" });
  saveWorkbook(wbout, "estatisticas.xlsx");
}

function getTableData(rows) {
  var data = [];
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    var rowData = [];

    // Adicionar os valores das estatísticas dos jogadores
    var cells = row.getElementsByTagName("td");
    var jogador = cells[0].querySelector("select").value;
    var estatisticas = [
      "gol",
      "finalizacaoTrave",
      "finalizacaoDefendida",
      "finalizacaoFora",
      "assistencia",
      "lancamentoLongo",
      "desarme",
      "faltaSofrida",
      "penaltiSofrido",
      "jogoSemSofrerGol",
      "defesa",
      "defesaPenalti",
      "golSofrido",
      "faltaCometida",
      "golContra",
      "cartaoAmarelo",
      "cartaoVermelho",
      "penaltiPerdido",
      "penaltiCometido",
    ];

    rowData.push(jogador);
    for (var j = 1; j < cells.length; j++) {
      var value = parseInt(cells[j].querySelector("span").textContent);
      rowData.push(value);
    }

    data.push(rowData);
  }
  return data;
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

jogadores.js;

var jogadores = [
  {
    nome: " ",
    gol: 0,
    finalizacaoTrave: 0,
    finalizacaoDefendida: 0,
    finalizacaoFora: 0,
    assistencia: 0,
    lancamentoLongo: 0,
    desarme: 0,
    faltaSofrida: 0,
    penaltiSofrido: 0,
    jogoSemSofrerGol: 0,
    defesa: 0,
    defesaPenalti: 0,
    golSofrido: 0,
    faltaCometida: 0,
    golContra: 0,
    cartaoAmarelo: 0,
    cartaoVermelho: 0,
    penaltiPerdido: 0,
    penaltiCometido: 0,
  },
];

var goleiros = [
  {
    nome: " ",
    gol: 0,
    finalizacaoTrave: 0,
    finalizacaoDefendida: 0,
    finalizacaoFora: 0,
    assistencia: 0,
    lancamentoLongo: 0,
    desarme: 0,
    faltaSofrida: 0,
    penaltiSofrido: 0,
    jogoSemSofrerGol: 0,
    defesa: 0,
    defesaPenalti: 0,
    golSofrido: 0,
    faltaCometida: 0,
    golContra: 0,
    cartaoAmarelo: 0,
    cartaoVermelho: 0,
    penaltiPerdido: 0,
    penaltiCometido: 0,
  },
];

function criarCelulaEstatistica(jogador, estatistica) {
  var td = document.createElement("td");

  var buttonContainer = document.createElement("div");
  buttonContainer.classList.add("button-container");

  var minusButton = document.createElement("button");
  minusButton.textContent = "-1";
  minusButton.classList.add("minus-button");
  minusButton.addEventListener("click", function () {
    decrementar(jogador, estatistica, td);
  });

  var valueSpan = document.createElement("span");
  valueSpan.textContent = jogador[estatistica];

  var plusButton = document.createElement("button");
  plusButton.textContent = "+1";
  plusButton.addEventListener("click", function () {
    incrementar(jogador, estatistica, td);
  });

  buttonContainer.appendChild(minusButton);
  buttonContainer.appendChild(valueSpan);
  buttonContainer.appendChild(plusButton);

  td.appendChild(buttonContainer);

  return td;
}