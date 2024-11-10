import os
import django
import random
from faker import Faker
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from myapp.models import Filial, Responsavel, Crianca, Atividade, Participacao, Necessidade_especial

fake = Faker('pt_BR')

def create_filial():
    unidades = [Filial.UNIDADE_1, Filial.UNIDADE_2]
    for unidade in unidades:
        Filial.objects.create(nome=unidade)

def create_responsavel(n):
    responsaveis = []
    for _ in range(n):
        responsavel = Responsavel.objects.create(
            nome=fake.name(),
            telefone=fake.random_number(digits=11, fix_len=True),
            email=fake.email(),
            profissao=fake.job(),
            local_de_trabalho=fake.company(),
            grau_de_parentesco=fake.random_element(elements=('Pai', 'Mãe', 'Tio', 'Tia', 'Avô', 'Avó'))
        )
        responsaveis.append(responsavel)
    return responsaveis

def create_necessidade_especial(n):
    necessidades = []
    for _ in range(n):
        necessidade = Necessidade_especial.objects.create(
            descricao=fake.sentence(nb_words=6)
        )
        necessidades.append(necessidade)
    return necessidades

def create_crianca(n, responsaveis, necessidades):
    filiais = Filial.objects.all()
    for _ in range(n):
        crianca = Crianca.objects.create(
            nome=fake.name(),
            data_de_nascimento=fake.date_of_birth(minimum_age=3, maximum_age=12),
            tamanho_camiseta=fake.random_element(elements=('P', 'M', 'G', 'GG')),
            escola=fake.company(),
            turno=fake.random_element(elements=('Matutino', 'Vespertino', 'Noturno', 'Integral')),
            rua=fake.street_name(),
            numero=fake.building_number(),
            bairro=fake.city(),
            cep=fake.random_number(digits=8, fix_len=True),
            telefone_responsavel=fake.random_number(digits=11, fix_len=True),
            filial=random.choice(filiais),
            necessidade_especial=random.choice(necessidades)
        )
        crianca.responsavel.set(random.sample(responsaveis, k=random.randint(1, 3)))
        crianca.save()

def create_atividade(n):
    for _ in range(n):
        Atividade.objects.create(
            nome=fake.word()
        )

def create_participacao(n):
    criancas = Crianca.objects.all()
    atividades = Atividade.objects.all()
    for _ in range(n):
        crianca = random.choice(criancas)
        atividade = random.choice(atividades)
        data_inicio = fake.date_this_year()
        data_fim = data_inicio + timedelta(days=random.randint(1, 30))
        Participacao.objects.create(
            nome=crianca,
            atividade=atividade,
            data_inicio=data_inicio,
            data_fim=data_fim,
            status=fake.random_element(elements=('INSCRITA', 'CONCLUIDA', 'CANCELADA'))
        )

if __name__ == '__main__':
    try:
        print("Populando o banco de dados... Aguarde.")
        create_filial()
        responsaveis = create_responsavel(10)
        necessidades = create_necessidade_especial(5)
        create_crianca(10, responsaveis, necessidades)
        create_atividade(5)
        create_participacao(20)
        print("População concluída.")
    except Exception as e:
        print(f"Erro ao popular o banco de dados: {e}")