from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Jogador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    posicao = db.Column(db.String(20), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey('time.id'))

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    jogadores = db.relationship('Jogador', backref='time', lazy=True)

class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time1_id = db.Column(db.Integer, db.ForeignKey('time.id'), nullable=False)
    time2_id = db.Column(db.Integer, db.ForeignKey('time.id'), nullable=False)
    vitorias_time1 = db.Column(db.Integer, default=0)
    vitorias_time2 = db.Column(db.Integer, default=0)
    empates = db.Column(db.Integer, default=0)
