// chatgpt responda em pt-br essa é a pelada.js 

// Função para atualizar o temporizador
function atualizarTemporizador() {
    var temporizadorElemento = document.getElementById('temporizador');
    var tempoRestante = 600; // 10 minutos em segundos

    var temporizadorInterval = setInterval(function() {
        var minutos = Math.floor(tempoRestante / 60);
        var segundos = tempoRestante % 60;

        // Formata os minutos e segundos com dois dígitos
        var minutosFormatados = minutos < 10 ? '0' + minutos : minutos;
        var segundosFormatados = segundos < 10 ? '0' + segundos : segundos;

        // Atualiza o texto do temporizador
        temporizadorElemento.textContent = minutosFormatados + ':' + segundosFormatados;

        // Decrementa o tempo restante
        tempoRestante--;

        // Verifica se o temporizador chegou a 0
        if (tempoRestante < 0) {
            clearInterval(temporizadorInterval);
            temporizadorElemento.textContent = 'Tempo esgotado';
            // Adicione aqui as ações a serem executadas quando o tempo acabar
        }
    }, 1000); // Executa a cada segundo
}

// Inicia o temporizador quando a página é carregada
window.onload = function() {
    atualizarTemporizador();
};

function exibirSubpagina(subpagina) {
    // Oculta todas as subpáginas
    var subpaginas = document.querySelectorAll('.subpagina');
    subpaginas.forEach(function (element) {
        element.style.display = 'none';
    });

    // Exibe a subpágina selecionada
    var subpaginaSelecionada = document.getElementById(subpagina);
    subpaginaSelecionada.style.display = 'block';
}

