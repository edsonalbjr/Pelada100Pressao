from flask import Flask, render_template, request, redirect, url_for
from models import db, Jogador, Time, Partida

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Criação das tabelas no banco de dados
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        nota = request.form['nota']
        posicao = request.form['posicao']
        novo_jogador = Jogador(nome=nome, nota=nota, posicao=posicao)
        db.session.add(novo_jogador)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastro.html')


@app.route('/gerenciamento')
def gerenciamento():
    times = Time.query.all()
    partidas = Partida.query.all()
    return render_template('gerenciamento.html', times=times, partidas=partidas)


if __name__ == '__main__':
    app.run(debug=True)
