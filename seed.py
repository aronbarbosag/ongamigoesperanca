import os
import django
import random
from faker import Faker
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.models import Crianca, Atividade, Participacao

fake = Faker('pt_BR')

def create_atividade():
    return Atividade.objects.create(
        nome=fake.word()
    )

def create_crianca():
    return Crianca.objects.create(
        nome=fake.name(),
        data_de_nascimento=fake.date_of_birth(minimum_age=3, maximum_age=12),
        tamanho_camiseta=fake.random_element(elements=('P', 'M', 'G', 'GG')),
        escola=fake.company(),
        turno=fake.random_element(elements=('Matutino', 'Vespertino', 'Noturno', 'Integral')),
        rua=fake.street_name(),
        numero=fake.building_number(),
        bairro=fake.city(),
        cep=fake.random_number(digits=8, fix_len=True),
        telefone_responsavel=fake.random_number(digits=11, fix_len=True)
    )

def create_participacao(crianca, atividade):
    data_inicio = fake.date_this_year()
    data_fim = data_inicio + timedelta(days=random.randint(1, 30))
    return Participacao.objects.create(
        nome=crianca,
        atividade=atividade,
        data_inicio=data_inicio,
        data_fim=data_fim,
        status=fake.random_element(elements=('INSCRITA', 'CONCLUIDA', 'CANCELADA'))
    )

def populate(n):
    atividades = [create_atividade() for _ in range(5)]
    for _ in range(n):
        crianca = create_crianca()
        atividade = random.choice(atividades)
        create_participacao(crianca, atividade)

if __name__ == '__main__':
    try:
        print("Populando o banco de dados... Aguarde.")
        populate(100)
        print("População concluída.")
    except Exception as e:
        print(f"Erro ao popular o banco de dados: {e}")