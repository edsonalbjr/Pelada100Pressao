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
    "Time 1": "T1",
    "Menos Velozes e Menos Furiosos": "MVMF",
    "Time 3": "T3",
    "Time 4": "T4",
    "Esquadrão Homicida": "EH",
    "Time 6": "T6",
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
          <button class="goal-button" ${
            matchInProgress ? "" : "disabled"
          }>Gol</button>
          <span class="goals-scored">0</span> Gols
          `;

    const goalButton = playerStat.querySelector(".goal-button");
    const goalsScored = playerStat.querySelector(".goals-scored");

    goalButton.addEventListener("click", function () {
      if (matchInProgress) {
        goalsScored.textContent = parseInt(goalsScored.textContent) + 1;
        updateScore(team1Abbreviation, team2Abbreviation); // Certifique-se de passar as abreviações corretas aqui
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
