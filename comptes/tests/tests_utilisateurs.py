from django.test import TestCase

from django.contrib.auth import get_user_model


class TestUser(TestCase):
    matricule = "JohnDoe04"
    email = "JohnDoe04@gmail.com"
    nom = "John"
    prenoms = "Doe"
    telephone = "0153636709"
    password = "RandomPassword"

    def setUp(self) -> None:
        get_user_model().objects.create(
            matricule=self.matricule, nom=self.nom,
            prenoms=self.prenoms, telephone=self.telephone,
            password=self.password
        )

    def test_user_retrieval_incorrect_format(self):
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(email=self.email)

    def test_user_retrieval_incorrect_format_with_lowercase(self):
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(email=self.email.lower())

    def test_user_retrieval(self):
        user = get_user_model().objects.get(matricule=self.matricule)
        assert user.prenoms == self.prenoms

    def test_user_update(self):
        user = get_user_model().objects.get(matricule=self.matricule)
        user.is_active = False
        user.save()
        user.refresh_from_db()
        self.assertNotEqual(user.is_active, True)

    def test_user_delete(self):
        user = get_user_model().objects.get(telephone=self.telephone)
        user.delete()
        with self.assertRaises(Exception) as exc:
            get_user_model().objects.get(telephone=self.telephone)

        self.assertEqual(type(exc.exception), get_user_model().DoesNotExist)
