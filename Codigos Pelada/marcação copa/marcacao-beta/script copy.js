document.addEventListener("DOMContentLoaded", function () {
  const team1Select = document.getElementById("team1");
  const team2Select = document.getElementById("team2");
  const startMatchButton = document.getElementById("start-match");
  const endMatchButton = document.getElementById("end-match");
  const scoreDisplay = document.querySelector(".score");
  const pauseMatchButton = document.getElementById("pause-match");
  const resumeMatchButton = document.getElementById("resume-match");

  let matchPaused = false;
  const team1Name = "Casa";
  const team2Name = "Visitante";

  const teams = {
    team1: [
      "Leandro",
      "Diego",
      "Eric",
      "Henrique Souza",
      "Kiel",
      "Matheus",
      "Nagibio",
      "Thiago Alemão",
      "Victor Assis",
    ],
    team2: [
      "Borel",
      "Bidu",
      "Jackson",
      "Lázaro",
      "Lucas Paranhos",
      "Lucas Silveira",
      "Teixa",
      "Vinícius",
      "Vitor Salgado",
    ],
    team3: [
      "Japa",
      "Dato",
      "Felipe Melo",
      "Gabriel Ferreira",
      "Juninho",
      "Marcelinho",
      "Paulo Thiago",
      "Victor Cabeça",
      "Winnicius C.",
    ],
    team4: [
      "Uili",
      "Christopher",
      "Elvinho",
      "Grimauro",
      "Icaro F.",
      "Jefferson",
      "Jorge",
      "Manga",
      "Raphael Borges",
    ],
    team5: [
      "Riva",
      "Albert",
      "Betinho",
      "Bruno P.",
      "Gil",
      "Marquinhos",
      "Nicláudio",
      "Pou",
      "Teteca",
    ],
    team6: [
      "Serginho",
      "Alysson Pink",
      "Duduzinho",
      "Eduardo",
      "Flávio",
      "Henrique S.",
      "Lucas Henrique",
      "Pedro",
      "Rafa Ribeiro",
    ],
  };

  let matchInProgress = false;
  let selectedTeam1Name = "";
  let selectedTeam2Name = "";
  let team1Abbreviation = ""; // Variável global
  let team2Abbreviation = ""; // Variável global

  // Defina as abreviações dos times aqui
  const teamAbbreviations = {
    "Cães de Guerra": "CG",
    "100 Pressão": "100P",
    "Prime Esportes": "PE",
    "Amigos do Futebol": "AF",
    "Esquadrão Homicida": "EH",
    "Zebra FC": "ZFC",
  };

  // cronometro

  let matchTime = 0; // Tempo total decorrido (em segundos)
  let timerInterval; // Identificador do intervalo de atualização do cronômetro

  // Código para atualizar o placar...
  updateScore(team1Abbreviation, team2Abbreviation);

  // Função para atualizar a tabela de times
  function updateTeamTable() {
    const team1Goals = calculateTotalGoalsByTeam(".team-stats-left");
    const team2Goals = calculateTotalGoalsByTeam(".team-stats-right");
    const tableBody = document.getElementById("table-body");
    tableBody.innerHTML = "";

    // Para cada time, crie uma nova linha na tabela
    for (const team in teams) {
      const teamRow = document.createElement("tr");
      const teamNameCell = document.createElement("td");
      const teamPointsCell = document.createElement("td");
      const teamGoalsCell = document.createElement("td");

      teamNameCell.textContent = team;
      teamPointsCell.textContent = calculateTeamPoints(team); // Atualize de acordo com sua lógica
      teamGoalsCell.textContent = calculateTotalGoalsByTeam(team);

      teamRow.appendChild(teamNameCell);
      teamRow.appendChild(teamPointsCell);
      teamRow.appendChild(teamGoalsCell);

      tableBody.appendChild(teamRow);
    }
  }

  // Função para calcular os pontos de um time
  function calculateTeamPoints(team) {
    // Sua lógica para calcular os pontos aqui
    return 0;
  }

  // Função para calcular o total de gols marcados por um time
  function calculateTotalGoalsByTeam(teamSelector) {
    const goalsElements = document.querySelectorAll(
      teamSelector + " .goals-scored"
    );
    let totalGoals = 0;

    goalsElements.forEach((element) => {
      totalGoals += parseInt(element.textContent);
    });

    return totalGoals;
  }

  // Chame a função para atualizar a tabela de times
  updateTeamTable();

  // Atualiza o cronômetro
  const timerDisplay = document.getElementById("cronometro");
  timerDisplay.textContent = formatTime(matchTime);

  function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    const formattedMinutes = minutes.toString().padStart(2, "0");
    const formattedSeconds = remainingSeconds.toString().padStart(2, "0");
    return `${formattedMinutes}:${formattedSeconds}`;
  }

  // cronometro

  // botões ocultos
  function updateButtonState() {
    startMatchButton.style.display = matchInProgress ? "none" : "block";
    pauseMatchButton.style.display =
      matchInProgress && !matchPaused ? "block" : "none";
    resumeMatchButton.style.display =
      matchInProgress && matchPaused ? "block" : "none";
    endMatchButton.style.display = matchInProgress ? "block" : "none";
  }

  updateButtonState();
  // botões ocultos

  startMatchButton.addEventListener("click", function () {
    if (!matchInProgress) {
      // Iniciar uma nova partida
      matchInProgress = true;
      startMatchButton.disabled = true;
      pauseMatchButton.disabled = false;
      endMatchButton.disabled = false;

      // Zerar o cronômetro
      matchTime = 0;
      timerDisplay.textContent = "00:00";

      // Iniciar o cronômetro
      timerInterval = setInterval(function () {
        matchTime++;
        timerDisplay.textContent = formatTime(matchTime);
      }, 1000);

      const team1 = team1Select.value;
      const team2 = team2Select.value;

      const teamStatsLeftContainer = document.querySelector(".team-stats-left");
      const teamStatsRightContainer =
        document.querySelector(".team-stats-right");

      teamStatsLeftContainer.innerHTML = "";
      teamStatsRightContainer.innerHTML = "";

      const team1Title = document.createElement("h2");
      team1Title.textContent = team1Name;
      teamStatsLeftContainer.appendChild(team1Title);

      const team2Title = document.createElement("h2");
      team2Title.textContent = team2Name;
      teamStatsRightContainer.appendChild(team2Title);

      const team1Index = team1Select.selectedIndex;
      const team2Index = team2Select.selectedIndex;

      selectedTeam1Name = team1Select.options[team1Index].text;
      selectedTeam2Name = team2Select.options[team2Index].text;

      team1Abbreviation = teamAbbreviations[selectedTeam1Name];
      team2Abbreviation = teamAbbreviations[selectedTeam2Name];

      for (let i = 0; i < teams[team1].length; i++) {
        const player1 = teams[team1][i];
        const player2 = teams[team2][i];

        const playerStat1 = createPlayerStat(player1);
        const playerStat2 = createPlayerStat(player2);

        teamStatsLeftContainer.appendChild(playerStat1);
        teamStatsRightContainer.appendChild(playerStat2);
      }

      updateScore(team1Abbreviation, team2Abbreviation);
    } else if (!matchPaused) {
      // Pausar a partida
      matchPaused = true;
      pauseMatchButton.disabled = true;
      resumeMatchButton.disabled = false;
      endMatchButton.disabled = true; // Você pode desativar o botão "Parar" quando a partida estiver pausada

      // Pausar o cronômetro
      clearInterval(timerInterval);
    } else {
      // Retomar a partida pausada
      matchPaused = false;
      pauseMatchButton.disabled = false;
      resumeMatchButton.disabled = true;
      endMatchButton.disabled = false; // Ative novamente o botão "Parar"

      // Retomar o cronômetro
      timerInterval = setInterval(function () {
        matchTime++;
        timerDisplay.textContent = formatTime(matchTime);
      }, 1000);
    }
    updateButtonState();
  });

  pauseMatchButton.addEventListener("click", function () {
    // Pausar a partida
    pauseMatchButton.disabled = true;
    resumeMatchButton.disabled = false;
    matchPaused = true;

    // Pausar o cronômetro
    clearInterval(timerInterval);
    updateButtonState();
  });

  resumeMatchButton.addEventListener("click", function () {
    // Retomar a partida pausada
    pauseMatchButton.disabled = false;
    resumeMatchButton.disabled = true;
    matchPaused = false;

    // Retomar o cronômetro
    timerInterval = setInterval(function () {
      matchTime++;
      timerDisplay.textContent = formatTime(matchTime);
    }, 1000);
    updateButtonState();
  });

  endMatchButton.addEventListener("click", function () {
    // Encerrar a partida
    matchInProgress = false;
    matchPaused = false;
    startMatchButton.disabled = false;
    pauseMatchButton.disabled = true;
    resumeMatchButton.disabled = true;
    endMatchButton.disabled = true;

    // Zerar o cronômetro
    matchTime = 0;
    clearInterval(timerInterval);
    timerDisplay.textContent = "00:00";

    const goalsTeam1 = calculateTotalGoals(".team-stats-left .goals-scored");
    const goalsTeam2 = calculateTotalGoals(".team-stats-right .goals-scored");

    let matchResult = "Empate";

    if (goalsTeam1 > goalsTeam2) {
      matchResult = `${selectedTeam1Name} ganhou`;
    } else if (goalsTeam2 > goalsTeam1) {
      matchResult = `${selectedTeam2Name} ganhou`;
    }

    // Exiba o resultado da partida
    const resultContainer = document.querySelector(".score");
    resultContainer.textContent = matchResult;

    // Calcula pontos e atualiza placar, se necessário
    if (goalsTeam1 !== goalsTeam2) {
      // Atualize os pontos de acordo com a lógica do seu jogo
      // ...
    }

    updatePlayerRanking(); // Chama a função para atualizar a tabela de ranking
    updateButtonState(); // Atualiza os botões
  });

  function createPlayerStat(player, team) {
    const playerStat = document.createElement("div");
    playerStat.className = `player-stat ${team}-player-${player}`;
    playerStat.innerHTML = `
     <h3>${player}</h3>
     <button class="goal-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Gol</button>
     <button class="assist-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Assistência</button>
     <button class="shot-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Finalização</button>
     <button class="on-target-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Finalização no Gol</button>
     <button class="tackle-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Desarme</button>
     <button class="interception-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Interceptação</button>
     <button class="block-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Bloqueio</button>
     <button class="foul-suffered-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Falta Sofrida</button>
     <button class="penalty-suffered-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Pênalti Sofrido</button>
     <button class="penalty-missed-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Pênalti Perdido</button>
     <button class="yellow-card-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Cartão Amarelo</button>
     <button class="red-card-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Cartão Vermelho</button>
     <button class="own-goal-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Gol Contra</button>
     <button class="penalty-committed-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Pênalti Cometido</button>
     <button class="foul-committed-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Falta Cometida</button>
     <button class="save-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Defesa</button>
     <button class="clean-sheet-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Jogo sem Sofrer Gol</button>
     <button class="penalty-save-button hidden" ${
       matchInProgress ? "" : "disabled"
     }>Defesa Pênalti</button>
     <span class="goals-scored">0</span> Gols
     <span class="assists-scored">0</span> Assists
     <span class="shots-taken">0</span> Finalizações
     <span class="shots-on-target">0</span> Finalizações no Gol
     <span class="tackles-made">0</span> Desarmes
     <span class="interceptions-made">0</span> Interceptações
     <span class="blocks-made">0</span> Bloqueios
     <span class="fouls-suffered">0</span> Faltas Sofridas
     <span class="penalties-suffered">0</span> Pênaltis Sofridos
     <span class="penalties-missed">0</span> Pênaltis Perdidos
     <span class="yellow-cards">0</span> Cartões Amarelos
     <span class="red-cards">0</span> Cartões Vermelhos
     <span class="own-goals">0</span> Gols Contra
     <span class="penalties-committed">0</span> Pênaltis Cometidos
     <span class="fouls-committed">0</span> Faltas Cometidas
     <span class="saves-made">0</span> Defesas
     <span class="clean-sheets">0</span> Jogos sem Sofrer Gol
     <span class="penalty-saves">0</span> Defesas de Pênalti
     `;

    const statButtons = playerStat.querySelectorAll(
      ".goal-button, .assist-button, .shot-button, .on-target-button, " +
        ".tackle-button, .interception-button, .block-button, .foul-suffered-button, " +
        ".penalty-suffered-button, .penalty-missed-button, .yellow-card-button, " +
        ".red-card-button, .own-goal-button, .penalty-committed-button, " +
        ".foul-committed-button, .save-button, .clean-sheet-button, .penalty-save-button"
    );

    const playerNameElement = playerStat.querySelector("h3");
    playerNameElement.addEventListener("click", function () {
      // Alterna a visibilidade dos botões de estatísticas
      statButtons.forEach((button) => {
        button.classList.toggle("hidden");
      });
    });

    const goalButton = playerStat.querySelector(".goal-button");
    const assistButton = playerStat.querySelector(".assist-button");
    const shotButton = playerStat.querySelector(".shot-button");
    const onTargetButton = playerStat.querySelector(".on-target-button");
    const tackleButton = playerStat.querySelector(".tackle-button");
    const interceptionButton = playerStat.querySelector(".interception-button");
    const blockButton = playerStat.querySelector(".block-button");
    const foulSufferedButton = playerStat.querySelector(
      ".foul-suffered-button"
    );
    const penaltySufferedButton = playerStat.querySelector(
      ".penalty-suffered-button"
    );
    const penaltyMissedButton = playerStat.querySelector(
      ".penalty-missed-button"
    );
    const yellowCardButton = playerStat.querySelector(".yellow-card-button");
    const redCardButton = playerStat.querySelector(".red-card-button");
    const ownGoalButton = playerStat.querySelector(".own-goal-button");
    const penaltyCommittedButton = playerStat.querySelector(
      ".penalty-committed-button"
    );
    const foulCommittedButton = playerStat.querySelector(
      ".foul-committed-button"
    );
    const saveButton = playerStat.querySelector(".save-button");
    const cleanSheetButton = playerStat.querySelector(".clean-sheet-button");
    const penaltySaveButton = playerStat.querySelector(".penalty-save-button");

    goalButton.addEventListener("click", function () {
      if (matchInProgress) {
        const goalsElement = playerStat.querySelector(".goals-scored");
        goalsElement.textContent = parseInt(goalsElement.textContent) + 1;
        updateScore(team1Abbreviation, team2Abbreviation);
      }
    });

    assistButton.addEventListener("click", function () {
      if (matchInProgress) {
        const assistsElement = playerStat.querySelector(".assists-scored");
        assistsElement.textContent = parseInt(assistsElement.textContent) + 1;
        // Lógica para assistências
      }
    });

    shotButton.addEventListener("click", function () {
      if (matchInProgress) {
        const shotsElement = playerStat.querySelector(".shots-taken");
        shotsElement.textContent = parseInt(shotsElement.textContent) + 1;
        // Lógica para finalizações
      }
    });

    onTargetButton.addEventListener("click", function () {
      if (matchInProgress) {
        const onTargetElement = playerStat.querySelector(".shots-on-target");
        onTargetElement.textContent = parseInt(onTargetElement.textContent) + 1;
        // Lógica para finalizações no gol
      }
    });

    tackleButton.addEventListener("click", function () {
      if (matchInProgress) {
        const tacklesElement = playerStat.querySelector(".tackles-made");
        tacklesElement.textContent = parseInt(tacklesElement.textContent) + 1;
        // Lógica para desarmes
      }
    });

    interceptionButton.addEventListener("click", function () {
      if (matchInProgress) {
        const interceptionsElement = playerStat.querySelector(
          ".interceptions-made"
        );
        interceptionsElement.textContent =
          parseInt(interceptionsElement.textContent) + 1;
        // Lógica para interceptações
      }
    });

    blockButton.addEventListener("click", function () {
      if (matchInProgress) {
        const blocksElement = playerStat.querySelector(".blocks-made");
        blocksElement.textContent = parseInt(blocksElement.textContent) + 1;
        // Lógica para bloqueios
      }
    });

    foulSufferedButton.addEventListener("click", function () {
      if (matchInProgress) {
        const foulsSufferedElement =
          playerStat.querySelector(".fouls-suffered");
        foulsSufferedElement.textContent =
          parseInt(foulsSufferedElement.textContent) + 1;
        // Lógica para faltas sofridas
      }
    });

    penaltySufferedButton.addEventListener("click", function () {
      if (matchInProgress) {
        const penaltiesSufferedElement = playerStat.querySelector(
          ".penalties-suffered"
        );
        penaltiesSufferedElement.textContent =
          parseInt(penaltiesSufferedElement.textContent) + 1;
        // Lógica para pênaltis sofridos
      }
    });

    penaltyMissedButton.addEventListener("click", function () {
      if (matchInProgress) {
        const penaltiesMissedElement =
          playerStat.querySelector(".penalties-missed");
        penaltiesMissedElement.textContent =
          parseInt(penaltiesMissedElement.textContent) + 1;
        // Lógica para pênaltis perdidos
      }
    });

    yellowCardButton.addEventListener("click", function () {
      if (matchInProgress) {
        const yellowCardsElement = playerStat.querySelector(".yellow-cards");
        yellowCardsElement.textContent =
          parseInt(yellowCardsElement.textContent) + 1;
        // Lógica para cartões amarelos
      }
    });

    redCardButton.addEventListener("click", function () {
      if (matchInProgress) {
        const redCardsElement = playerStat.querySelector(".red-cards");
        redCardsElement.textContent = parseInt(redCardsElement.textContent) + 1;
        // Lógica para cartões vermelhos
      }
    });

    ownGoalButton.addEventListener("click", function () {
      if (matchInProgress) {
        const ownGoalsElement = playerStat.querySelector(".own-goals");
        ownGoalsElement.textContent = parseInt(ownGoalsElement.textContent) + 1;
        // Lógica para gols contra
      }
    });

    penaltyCommittedButton.addEventListener("click", function () {
      if (matchInProgress) {
        const penaltiesCommittedElement = playerStat.querySelector(
          ".penalties-committed"
        );
        penaltiesCommittedElement.textContent =
          parseInt(penaltiesCommittedElement.textContent) + 1;
        // Lógica para pênaltis cometidos
      }
    });

    foulCommittedButton.addEventListener("click", function () {
      if (matchInProgress) {
        const foulsCommittedElement =
          playerStat.querySelector(".fouls-committed");
        foulsCommittedElement.textContent =
          parseInt(foulsCommittedElement.textContent) + 1;
        // Lógica para faltas cometidas
      }
    });

    saveButton.addEventListener("click", function () {
      if (matchInProgress) {
        const savesMadeElement = playerStat.querySelector(".saves-made");
        savesMadeElement.textContent =
          parseInt(savesMadeElement.textContent) + 1;
        // Lógica para defesas
      }
    });

    cleanSheetButton.addEventListener("click", function () {
      if (matchInProgress) {
        const cleanSheetsElement = playerStat.querySelector(".clean-sheets");
        cleanSheetsElement.textContent =
          parseInt(cleanSheetsElement.textContent) + 1;
        // Lógica para jogos sem sofrer gol
      }
    });

    penaltySaveButton.addEventListener("click", function () {
      if (matchInProgress) {
        const penaltySavesElement = playerStat.querySelector(".penalty-saves");
        penaltySavesElement.textContent =
          parseInt(penaltySavesElement.textContent) + 1;
        // Lógica para defesas de pênalti
      }
    });

    return playerStat;
  }

  function updateScore(team1Abbreviation, team2Abbreviation) {
    const goalsTeam1 = calculateTotalGoals(".team-stats-left .goals-scored");
    const goalsTeam2 = calculateTotalGoals(".team-stats-right .goals-scored");

    // console.log("Goals Team 1:", goalsTeam1);
    // console.log("Goals Team 2:", goalsTeam2);

    scoreDisplay.textContent = `${team1Abbreviation} ${goalsTeam1} x ${goalsTeam2} ${team2Abbreviation}`;
    // console.log("Team 1 Abbreviation:", team1Abbreviation);
    // console.log("Team 2 Abbreviation:", team2Abbreviation);
  }

  function calculateTotalGoals(selector) {
    const goalsElements = document.querySelectorAll(selector);
    let totalGoals = 0;

    goalsElements.forEach((element) => {
      totalGoals += parseInt(element.textContent);
    });

    return totalGoals;
  }
});

const team1Select = document.getElementById("team1");
const team2Select = document.getElementById("team2");

team1Select.addEventListener("change", function () {
  const selectedTeam1 = team1Select.value;
  const selectedTeam2 = team2Select.value;

  if (selectedTeam1 === selectedTeam2) {
    // Seleção repetida, atualiza a seleção do outro menu
    if (selectedTeam2 === "team1") {
      team2Select.value = "team2";
    } else {
      team2Select.value = "team1";
    }
  }
});

team2Select.addEventListener("change", function () {
  const selectedTeam1 = team1Select.value;
  const selectedTeam2 = team2Select.value;

  if (selectedTeam2 === selectedTeam1) {
    // Seleção repetida, atualiza a seleção do outro menu
    if (selectedTeam1 === "team1") {
      team1Select.value = "team2";
    } else {
      team1Select.value = "team1";
    }
  }
});

// RANKING

const rankingTableBody = document.getElementById("ranking-table-body");

function updatePlayerRanking() {
  const allPlayerStats = document.querySelectorAll(".player-stat");
  const playerStatsArray = Array.from(allPlayerStats);

  const playerRanking = playerStatsArray.map((playerStat) => {
    const playerName = playerStat.querySelector("h3").textContent;
    const goalsScored = parseInt(
      playerStat.querySelector(".goals-scored").textContent
    );
    return { playerName, goalsScored };
  });

  playerRanking.sort((a, b) => b.goalsScored - a.goalsScored);

  rankingTableBody.innerHTML = ""; // Limpa a tabela de ranking

  const maxPlayersToShow = 50; // Defina o número máximo de jogadores a serem exibidos

  for (let i = 0; i < Math.min(playerRanking.length, maxPlayersToShow); i++) {
    const player = playerRanking[i];
    const row = document.createElement("tr");
    row.innerHTML = `
       <td>${i + 1}. ${player.playerName}</td>
       <td>${player.goalsScored}</td>
     `;
    rankingTableBody.appendChild(row);
  }
}

updatePlayerRanking();
