# Generated by Django 4.1.3 on 2022-11-05 08:04

import comptes.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0002_alter_utilisateur_email'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='utilisateur',
            managers=[
                ('objects', comptes.models.Manager()),
            ],
        ),
    ]
