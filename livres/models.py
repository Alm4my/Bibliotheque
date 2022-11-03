from django.db import models
from simple_history.models import HistoricalRecords

import comptes.models


class Auteur(models.Model):
    nom = models.CharField(max_length=255)
    prenoms = models.CharField(max_length=255)


class Livre(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    titre = models.CharField(max_length=255)
    nombre = models.IntegerField()
    auteurs = models.ManyToManyField(Auteur, "livres")


class Commande(models.Model):
    matricule = models.OneToOneField(
        comptes.models.Utilisateur,
        models.DO_NOTHING,
        "matricule",
        primary_key=True
    )
    isbn_livre = models.ForeignKey(Livre, on_delete=models.DO_NOTHING)
    validee = models.BooleanField(default=False)
    date_debut = models.DateField(auto_now_add=True, blank=True)
    date_fin = models.DateField(blank=True, null=True)
    histoire = HistoricalRecords(table_name="livres_commandes_historique")
