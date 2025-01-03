# Generated by Django 5.1.3 on 2024-11-10 16:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Atividade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name_plural": "Cadastro das atividades",
            },
        ),
        migrations.CreateModel(
            name="Filial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome_filial", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Necessidade_especial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("descricao", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Responsavel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100, null=True)),
                ("telefone", models.IntegerField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("profissao", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "local_de_trabalho",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "grau_de_parentesco",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Crianca",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=20)),
                ("data_de_nascimento", models.DateField()),
                ("tamanho_camiseta", models.CharField(blank=True, max_length=20)),
                ("escola", models.CharField(blank=True, max_length=100)),
                (
                    "turno",
                    models.CharField(
                        choices=[
                            ("Matutino", "Matutino"),
                            ("Vespetino", "Vespetino"),
                            ("Noturno", "Noturno"),
                            ("Integral", "Integral"),
                        ],
                        max_length=9,
                    ),
                ),
                ("rua", models.CharField(blank=True, max_length=200)),
                ("numero", models.IntegerField(blank=True, null=True)),
                ("bairro", models.CharField(blank=True, max_length=100)),
                ("cep", models.CharField(blank=True, max_length=8)),
                ("telefone_responsavel", models.CharField(blank=True, max_length=11)),
                (
                    "filial",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT, to="myapp.filial"
                    ),
                ),
                (
                    "necessidade_especial",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="myapp.necessidade_especial",
                    ),
                ),
                ("responsavel", models.ManyToManyField(to="myapp.responsavel")),
            ],
            options={
                "verbose_name_plural": "Cadastro das crianças",
            },
        ),
        migrations.CreateModel(
            name="Participacao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data_inicio", models.DateField()),
                ("data_fim", models.DateField(blank=True, null=True)),
                ("status", models.CharField(default="INSCRITA", max_length=20)),
                (
                    "atividade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="myapp.atividade",
                    ),
                ),
                (
                    "nome",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="myapp.crianca"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Participações das crianças",
            },
        ),
    ]
