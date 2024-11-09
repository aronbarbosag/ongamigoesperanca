# Generated by Django 5.1a1 on 2024-11-09 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
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
                ("tamanho_camiseta", models.CharField(max_length=20)),
                ("escola", models.CharField(max_length=100)),
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
                ("rua", models.CharField(max_length=200)),
                ("numero", models.IntegerField()),
                ("bairro", models.CharField(max_length=100)),
                ("cep", models.CharField(max_length=8)),
                ("telefone_responsavel", models.CharField(max_length=11)),
            ],
        ),
    ]
