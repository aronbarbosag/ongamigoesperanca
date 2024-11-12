from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator
import datetime

class Filial(models.Model):
    UNIDADE_1 = 'ERICH BELZ'
    UNIDADE_2 = 'VILA JENSEN'
    UNIDADE_CHOICE = ((UNIDADE_1,'ERICH BELZ'),(UNIDADE_2,'VILA JENSEN'))
    
    nome_filial = models.CharField(max_length=100,choices=UNIDADE_CHOICE,null=True,blank=True)

    def __str__(self):
        return self.nome_filial


class Necessidade_especial(models.Model):
    descricao = models.CharField(max_length=200)
    
    def __str__(self):
        return self.descricao
    


class Responsavel(models.Model):
    nome = models.CharField(max_length=100, null=True)
    telefone = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profissao = models.CharField(max_length=100, blank=True, null=True)
    local_de_trabalho = models.CharField(max_length=200, blank=True, null=True)
    grau_de_parentesco = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome


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
    turno = models.CharField(max_length=9, choices=TURN_CHOICES, blank=True,null=True)
    rua = models.CharField(max_length=200, blank=True)
    numero = models.IntegerField(blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=8, blank=True)
    telefone_responsavel = models.CharField(max_length=11, blank=True)
    responsavel = models.ManyToManyField(Responsavel)
    filial = models.ForeignKey(Filial,on_delete=models.PROTECT,blank=True,null=True)
    necessidade_especial = models.ForeignKey(Necessidade_especial,on_delete=models.SET_NULL,blank=True,null=True)
    
    @property
    def nomes_responsaveis(self):
        return ", ".join([responsavel.nome for responsavel in self.responsavel.all()])
    
    @property
    def responsavel_grau_de_parentesco(self):
        return ", ".join([responsavel.grau_de_parentesco for responsavel in self.responsavel.all()])
    
    @property
    def nome_filial(self):
        return self.filial.nome_filial if self.filial else "Sem Filial"
    
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

    def nome_crianca(self):
        return self.nome.nome
    nome_crianca.admin_order_field = 'nome'
    nome_crianca.short_description = 'Nome da Criança'