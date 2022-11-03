from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from comptes.models import Utilisateur


class CreateUserForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = (
            "nom", "prenoms", "matricule", "email", "telephone", "password1", "password2"
        )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username: str = self.cleaned_data.get('username')
        password: str = self.cleaned_data.get('password')
        user: Utilisateur = Utilisateur.objects.filter(
            Q(matricule=username) |
            Q(telephone=username) |
            Q(email=username)
        ).first()
        if user and user.is_active and user.check_password(password):
            return self.cleaned_data

        raise forms.ValidationError(
            'Vos identifiants sont invalides. Veuillez '
            're-essayer.'
            )

    def login(self, request):
        user: Utilisateur = authenticate(
            username=self.cleaned_data.get('username'),
            password=self.cleaned_data.get('password')
        )
        if user:
            login(request, user, 'comptes.backends.AuthBackend')
            return 1
        return 0
