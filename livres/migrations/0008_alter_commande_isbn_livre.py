# Generated by Django 4.1.3 on 2022-11-05 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('livres', '0007_remove_commande_etat_emprunt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='isbn_livre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livres.livre'),
        ),
    ]
