from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models


class Manager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


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
    email = models.EmailField(
        "adresse email",
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w\d_\-.]+@inphb.ci$',
                message='Vous devez utiliser un email qui se termine par @inphb.ci',
                code='noinp'
            )
        ]
    )

    # Attributs désactivés remplacer par des attributs en francais.
    username = None
    first_name = None
    last_name = None

    # Le champ utilisé comme nom d'utilisateur
    USERNAME_FIELD = "matricule"
    objects = Manager()
