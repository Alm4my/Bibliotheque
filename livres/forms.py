from django import forms

from livres import models


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = models.Auteur
        fields = "__all__"


class AddBookForm(forms.ModelForm):
    class Meta:
        model = models.Livre
        fields = "__all__"


class AddCommandeForm(forms.ModelForm):
    class Meta:
        model = models.Commande
        fields = ('note',)
