# Generated by Django 5.1.3 on 2024-11-09 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pix', '0003_alter_pagamento_options_pagamento_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='qr_code',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='QR Code'),
        ),
    ]