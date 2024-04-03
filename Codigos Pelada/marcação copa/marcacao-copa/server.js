const express = require("express");
const path = require("path");

const app = express();
const port = 3000; // Pode ser outro número de porta se necessário

app.use(express.static(path.join(__dirname, "public")));

app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});

const fs = require('fs');

app.get('/estatisticas', (req, res) => {
  fs.readFile('estatisticas.txt', 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      return res.status(500).send('Erro ao ler as estatísticas.');
    }
    return res.send(data);
  });
});

app.post('/salvar-estatisticas', express.json(), (req, res) => {
    const estatisticas = req.body.estatisticas;
  
    fs.writeFile('estatisticas.txt', estatisticas, 'utf8', (err) => {
      if (err) {
        console.error(err);
        return res.status(500).send('Erro ao salvar as estatísticas.');
      }
      return res.send('Estatísticas salvas com sucesso.');
    });
  });

  
  