from django.db import models
from django.contrib.auth.models import User

class Pelada(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()
    local = models.CharField(max_length=100)

class Jogador(models.Model):
    pelada = models.ForeignKey(Pelada, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    apelido = models.CharField(max_length=100)
    posicao1 = models.CharField(max_length=50)
    posicao2 = models.CharField(max_length=50)
    nivel_habilidade = models.IntegerField(default=0)

class Estatisticas(models.Model):
    jogador = models.OneToOneField(Jogador, on_delete=models.CASCADE)
    jogos = models.IntegerField(default=0)
    vitorias = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    gols = models.IntegerField(default=0)
    assistencias = models.IntegerField(default=0)
