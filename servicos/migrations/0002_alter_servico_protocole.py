# Generated by Django 4.2.5 on 2024-06-01 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='protocole',
            field=models.CharField(blank=True, max_length=52, null=True),
        ),
    ]
