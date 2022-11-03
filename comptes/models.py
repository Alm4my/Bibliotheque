from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    """
    Classe Utilisateur

    Cette classe cree deux types d'utilisateurs les gérants de la bibliothèque et les
    étudiants.
    """
    matricule = models.CharField(
        "matricule de l'utilisateur", unique=True, null=True, blank=True, max_length=12
    )

    nom = models.CharField(
        "Nom de l'utilisateur", max_length=128
    )

    prenoms = models.CharField(
        "prenoms de l'utilisateur", max_length=255
    )

    telephone = models.CharField(
        "Numéro de telephone de l'utilisateur", max_length=10, unique=True
    )

    # Attributs désactivés remplacer par des attributs en francais.
    username = None
    first_name = None
    last_name = None

    # Le champ utilisé comme nom d'utilisateur
    USERNAME_FIELD = "matricule"

