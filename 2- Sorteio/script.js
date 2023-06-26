import jogadores from "./jogadores.js"; // Importa a lista de jogadores do arquivo jogadores.js

const listaJogadores = document.querySelector(".lista-jogadores"); // Obtém a referência da lista de jogadores na página
const listaSorteio = document.querySelector(".lista-sorteio"); // Obtém a referência da lista de jogadores para sorteio na página

// Função responsável por exibir os jogadores cadastrados na lista
function exibirJogadores() {
  listaJogadores.innerHTML = ""; // Limpa a lista de jogadores

  // Para cada jogador na lista de jogadores
  jogadores.forEach((jogador) => {
    const item = document.createElement("li"); // Cria um elemento de lista para cada jogador
    item.classList.add("jogador-item"); // Adiciona a classe CSS para estilização

    const jogadorInfo = document.createElement("div"); // Cria um elemento div para exibir as informações do jogador
    jogadorInfo.classList.add("jogador-info"); // Adiciona a classe CSS para estilização
    jogadorInfo.textContent = `${jogador.nome} - Estrelas: ${jogador.habilidade}`; // Define o texto das informações do jogador

    const botao = document.createElement("button"); // Cria um elemento de botão para adicionar/remover jogadores
    botao.classList.add("btn-acao"); // Adiciona a classe CSS para estilização

    // Verifica se o jogador já está na lista de sorteio
    if (jogador.adicionado) {
      botao.textContent = "Remover"; // Define o texto do botão como "Remover"
      botao.classList.add("btn-remover"); // Adiciona a classe CSS para estilização do botão de remoção
      botao.addEventListener("click", () => {
        jogador.adicionado = false; // Define a propriedade "adicionado" do jogador como false para removê-lo da lista de sorteio
        exibirJogadores(); // Atualiza a lista de jogadores
        exibirJogadoresSorteio(); // Atualiza a lista de jogadores para sorteio
      });
    } else {
      botao.textContent = "Adicionar"; // Define o texto do botão como "Adicionar"
      botao.classList.add("btn-adicionar"); // Adiciona a classe CSS para estilização do botão de adição
      botao.addEventListener("click", () => {
        jogador.adicionado = true; // Define a propriedade "adicionado" do jogador como true para adicioná-lo à lista de sorteio
        exibirJogadores(); // Atualiza a lista de jogadores
        exibirJogadoresSorteio(); // Atualiza a lista de jogadores para sorteio
      });
    }

    item.appendChild(jogadorInfo); // Adiciona as informações do jogador ao elemento de lista
    item.appendChild(botao); // Adiciona o botão de adicionar/remover ao elemento de lista
    listaJogadores.appendChild(item); // Adiciona o elemento de lista à lista de jogadores
  });
}

// Função responsável por exibir os jogadores na lista de sorteio
function exibirJogadoresSorteio() {
  listaSorteio.innerHTML = ""; // Limpa a lista de jogadores para sorteio

  let numeroJogadores = 0;
  let jogadoresAdicionados = [];
  let jogadoresOrdenados = jogadores
    .slice()
    .sort((jogador1, jogador2) => {
      return jogador1.nome.localeCompare(jogador2.nome);
    });

  jogadoresOrdenados.forEach((jogador) => {
    if (jogador.adicionado) {
      if (numeroJogadores < 25) {
        // Verifica se o número máximo de jogadores para sorteio foi atingido (25 jogadores)
        const item = document.createElement("li"); // Cria um elemento de lista para cada jogador adicionado
        item.textContent = `${jogador.nome} - Estrelas: ${jogador.habilidade}`; // Define o texto do item da lista como o nome e a habilidade do jogador
        listaSorteio.appendChild(item); // Adiciona o item à lista de jogadores para sorteio
        numeroJogadores++;
        jogadoresAdicionados.push(jogador);
      } else {
        alert("Os 25 jogadores já foram selecionados"); // Exibe um alerta informando que o número máximo de jogadores para sorteio foi atingido
        jogador.adicionado = false; // Define a propriedade "adicionado" do jogador como false para removê-lo da lista de sorteio
        jogadoresAdicionados.forEach((j) => {
          if (j !== jogador) {
            j.adicionado = true; // Define a propriedade "adicionado" dos outros jogadores como true para mantê-los na lista de sorteio
          }
        });
        exibirJogadores(); // Atualiza a lista de jogadores
        return;
      }
    }
  });
}

// Criação do botão de sorteio
const btnSortear = document.createElement("button");
btnSortear.textContent = "Sortear"; // Define o texto do botão como "Sortear"
btnSortear.classList.add("btn-sortear"); // Adiciona a classe CSS para estilização
listaSorteio.after(btnSortear); // Insere o botão de sorteio após a lista de jogadores para sorteio

btnSortear.addEventListener("click", sortearTimes); // Adiciona um evento de clique ao botão de sorteio para chamar a função sortearTimes

// Função chamada quando a página é carregada
document.addEventListener("DOMContentLoaded", () => {
  exibirJogadores(); // Exibe os jogadores cadastrados na lista
  exibirJogadoresSorteio(); // Exibe os jogadores para sorteio na lista
});

// Função responsável por sortear os times
function sortearTimes() {
  let jogadoresAdicionados = jogadores.filter(
    (jogador) => jogador.adicionado
  ); // Filtra os jogadores que foram adicionados à lista de sorteio

  // Embaralha os jogadores antes de ordená-los por habilidade
  jogadoresAdicionados.sort(() => Math.random() - 0.5);

  // Ordena os jogadores por habilidade em ordem decrescente
  jogadoresAdicionados.sort((a, b) => b.habilidade - a.habilidade);

  const numJogadores = jogadoresAdicionados.length;
  const numTimes = Math.ceil(numJogadores / 5); // Calcula o número de times necessário com base no número de jogadores

  const times = Array.from({ length: numTimes }, () => ({
    jogadores: [],
    pontuacao: 0,
  }));

  jogadoresAdicionados.forEach((jogador, index) => {
    let timeIndex;
    const remainder = index % numTimes;
    if (Math.floor(index / numTimes) % 2 === 0) {
      timeIndex = remainder;
    } else {
      timeIndex = numTimes - 1 - remainder;
    }

    times[timeIndex].jogadores.push(jogador); // Adiciona o jogador ao time correspondente
    times[timeIndex].pontuacao += jogador.habilidade; // Atualiza a pontuação do time com base na habilidade do jogador
  });

  // Embaralha os jogadores dentro de cada time
  times.forEach((time) => {
    time.jogadores.sort(() => Math.random() - 0.5);
  });

  // Embaralha os times
  times.sort(() => Math.random() - 0.5);

  const listaTimes = document.querySelector(".lista-times");
  listaTimes.innerHTML = "";

  times.forEach((time, index) => {
    const itemTime = document.createElement("li");
    itemTime.innerHTML = `<b>Time ${index + 1}: Estrelas: ${
      time.pontuacao
    }</b><br>`;
    const listaJogadoresTime = document.createElement("ol");

    time.jogadores.forEach((jogador) => {
      const itemJogador = document.createElement("li");
      itemJogador.innerHTML = `<b>${jogador.nome}</b> - Estrelas: ${jogador.habilidade}<br>`;
      listaJogadoresTime.appendChild(itemJogador);
    });

    itemTime.appendChild(listaJogadoresTime);
    itemTime.innerHTML += "<br>";
    listaTimes.appendChild(itemTime);
  });
}

// Chama a função sortearTimes
sortearTimes();

// Obtém o formulário para cadastrar jogadores
const formCadastrarJogador = document.querySelector(".cadastrar-jogador");

// Adiciona um evento de submit ao formulário
formCadastrarJogador.addEventListener("submit", (event) => {
  event.preventDefault(); // Impede o envio padrão do formulário

  const nome = document.querySelector("#nome").value; // Obtém o valor do campo de nome do jogador
  const habilidade = document.querySelector("#habilidade").value; // Obtém o valor do campo de habilidade do jogador

  const jogador = { nome, habilidade, adicionado: false }; // Cria um objeto jogador com os valores obtidos do formulário
  jogadores.push(jogador); // Adiciona o jogador à lista de jogadores

  exibirJogadores(); // Exibe os jogadores cadastrados na lista
});