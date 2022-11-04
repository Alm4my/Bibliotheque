from django.db import models
from simple_history.models import HistoricalRecords

import comptes.models


class Auteur(models.Model):
    nom = models.CharField(max_length=255)
    prenoms = models.CharField(max_length=255)

    class Meta:
        unique_together = ('nom', 'prenoms')

    def __str__(self):
        return f"{self.nom} {self.prenoms}"


class Livre(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    titre = models.CharField(max_length=255)
    nombre_de_copies = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)
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
    note = models.TextField(null=True, blank=True)
    histoire = HistoricalRecords(table_name="livres_commandes_historique")
