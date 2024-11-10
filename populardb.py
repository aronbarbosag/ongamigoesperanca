import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.models import Crianca, Responsavel

fake = Faker('pt_BR')

def create_responsavel():
    return Responsavel.objects.create(
        nome=fake.name(),
        telefone=fake.random_number(digits=11, fix_len=True),
        email=fake.email(),
        profissao=fake.job(),
        local_de_trabalho=fake.company(),
        grau_de_parentesco=fake.random_element(elements=('Pai', 'Mãe', 'Tio', 'Tia', 'Avô', 'Avó'))
    )

def link_responsavel_crianca(crianca, responsavel):
    crianca.responsavel.add(responsavel)
    crianca.save()

def populate_responsavel_and_link(n):
    responsaveis = [create_responsavel() for _ in range(n)]
    criancas = Crianca.objects.all()
    for crianca in criancas:
        responsavel = random.choice(responsaveis)
        link_responsavel_crianca(crianca, responsavel)

if __name__ == '__main__':
    try:
        print("Populando a tabela Responsavel e associando com Crianca... Aguarde.")
        populate_responsavel_and_link(10)
        print("População concluída.")
    except Exception as e:
        print(f"Erro ao popular o banco de dados: {e}")