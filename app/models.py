from django.db import models
from datetime import date


class Crianca(models.Model):
    MAT = "Matutino"
    VESP = "Vespetino"
    NOT = "Noturno"
    INT = "Integral"

    TURN_CHOICES = ((MAT, 'Matutino'), (VESP, 'Vespetino'),
                    (NOT, 'Noturno'), (INT, 'Integral'))
    nome = models.CharField(max_length=20)
    data_de_nascimento = models.DateField()
    tamanho_camiseta = models.CharField(max_length=20)
    escola = models.CharField(max_length=100)
    turno = models.CharField(max_length=9, choices=TURN_CHOICES)
    rua = models.CharField(max_length=200, blank=True)
    numero = models.IntegerField(null=True)
    bairro = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=8, blank=True)
    telefone_responsavel = models.CharField(max_length=11)

    def __str__(self):
        return self.nome

    # @property
    # def calculate_age(self):
    #     if self.idade:
    #         today = date.today()
    #         return today.year - self.data_de_nascimento.year
    #     return 0
