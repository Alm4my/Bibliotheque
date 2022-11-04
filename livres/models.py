from django.core.validators import RegexValidator
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
    isbn = models.CharField(
        max_length=13,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^(?=(?:.{10}|.{13})$)[0-9]*$',
                message='Seulement les chiffres sont acceptés. l\'isbn doit etre long '
                        'de 10 ou de 13 chiffres.',
                code='nomatch'
            )
        ]
    )
    titre = models.CharField(max_length=255)
    nombre_de_copies = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    auteurs = models.ManyToManyField(Auteur, "livres")

    def __str__(self):
        return f"{self.titre} - {self.auteurs.first()}"


class Commande(models.Model):
    # class EtatEmprunt(models.TextChoices):
    #     PREMIER_EMPRUNT = 'P', 'PREMIER EMPRUNT'
    #     LIVRE_NON_RENDU = 'N', 'LIVRE NON RENDU'
    #     LIVRE_RENDU = 'R', 'LIVRE RENDU'

    matricule = models.OneToOneField(
        comptes.models.Utilisateur,
        models.CASCADE,
        "matricule",
        primary_key=True
    )
    isbn_livre = models.ForeignKey(Livre, on_delete=models.DO_NOTHING)
    emprunt_en_cours = models.BooleanField(default=True)
    date_debut = models.DateField(auto_now_add=True, blank=True)
    date_fin = models.DateField(blank=True, null=True)
    note = models.TextField(null=True, blank=True)
    histoire = HistoricalRecords(table_name="livres_commandes_historique")

    def __str__(self):
        return f"Commande: {self.isbn_livre.titre} - {self.matricule.nom}"
