from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator
import datetime
# import django.utils.timezone.now


class Atividade(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Cadastro das atividades"

    def __str__(self):
        return self.nome


class Crianca(models.Model):
    MAT = "Matutino"
    VESP = "Vespetino"
    NOT = "Noturno"
    INT = "Integral"

    TURN_CHOICES = ((MAT, 'Matutino'), (VESP, 'Vespetino'),
                    (NOT, 'Noturno'), (INT, 'Integral'))
    nome = models.CharField(max_length=20)
    data_de_nascimento = models.DateField()
    tamanho_camiseta = models.CharField(max_length=20, blank=True)
    escola = models.CharField(max_length=100, blank=True)
    turno = models.CharField(max_length=9, choices=TURN_CHOICES)
    rua = models.CharField(max_length=200, blank=True)
    numero = models.IntegerField(blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=8, blank=True)
    telefone_responsavel = models.CharField(max_length=11, blank=True)

    @property
    def idade(self):
        # Calcula a idade dinamicamente
        today = datetime.date.today()
        return today.year - self.data_de_nascimento.year - (
            (today.month, today.day) < (
                self.data_de_nascimento.month, self.data_de_nascimento.day)
        )

    class Meta:
        verbose_name_plural = "Cadastro das crianças"

    def __str__(self):
        return self.nome


class Participacao(models.Model):
    nome = models.ForeignKey(Crianca, on_delete=models.PROTECT)
    atividade = models.ForeignKey(Atividade, on_delete=models.PROTECT)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default="INSCRITA")

    class Meta:
        verbose_name_plural = "Participações das crianças"
