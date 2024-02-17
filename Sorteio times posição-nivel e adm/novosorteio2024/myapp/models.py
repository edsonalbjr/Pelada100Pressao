# myapp/models.py
from django.db import models

class Jogador(models.Model):
    nome = models.CharField(max_length=255)
    habilidade = models.FloatField()
    adm = models.BooleanField(default=False)
    posicao_primaria = models.CharField(max_length=50)
    posicao_secundaria = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome
