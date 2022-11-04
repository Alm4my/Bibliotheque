import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import now

from comptes import permissions
from livres import forms, models
from livres.models import Commande as Cm
from util import messages as m


@user_passes_test(permissions.is_staff)
def add_author(request):
    form = forms.AddAuthorForm(request.POST or None)

    if request.method == 'GET':
        return render(request, 'auteur/creation.html', {'form': form})

    else:
        if form.is_valid():
            author: models.Auteur = form.save()
            messages.success(
                request,
                m.AUTHOR_CREATION_SUCCESS + f" Auteur: {author.nom} {author.prenoms}"
            )
            return render(
                request,
                'auteur/creation.html',
                {'form': forms.AddAuthorForm()}
            )

        messages.error(request, m.AUTHOR_CREATION_ERROR)
        return render(request, 'auteur/creation.html', {'form': form})


def add_book(request):
    form = forms.AddBookForm(request.POST or None)
    if request.user.is_staff and request.user.is_active:
        if request.method == "GET":
            return render(request, 'livre/creation.html', {'form': form})

        else:
            if form.is_valid():
                book: models.Livre = form.save()
                messages.success(
                    request,
                    m.BOOK_CREATION_SUCCESS + f"Livre: {book.titre} | ISBN: {book.isbn}"
                )
                return render(
                    request,
                    'livre/creation.html',
                    {'form': forms.AddBookForm()}
                )

            messages.error(request, m.BOOK_CREATION_ERROR)
            return render(request, 'livre/creation.html', {'form': form})
    messages.error(request, m.NOT_ENOUGH_RIGHTS)
    return redirect(f"{reverse('login')}?next={request.path}")


@login_required
def add_commande(request):
    form = forms.AddCommandeForm(request.POST or None)

    if request.method == 'GET':
        return render(request, 'livre/commande.html', {'form': form})

    else:
        com = models.Commande.objects.get(matricule=request.user.matricule)
        if (
                com.etat_emprunt == Cm.EtatEmprunt.PREMIER_EMPRUNT or
                com.etat_emprunt == Cm.EtatEmprunt.LIVRE_RENDU
        ):
            if form.is_valid():
                commande = form.save(commit=False)
                commande.matricule = request.user
                commande.date_debut = now()
                commande.date_fin = now() + datetime.timedelta(days=4)
                commande.etat_emprunt = models.Commande.EtatEmprunt.LIVRE_NON_RENDU
                commande.save()
                messages.success(request, m.COMMANDE_CREATION_SUCCESS)
                return redirect(reverse('home'))

        messages.error(request, m.COMMANDE_CREATION_ERROR_2)

        messages.error(request, m.COMMANDE_CREATION_ERROR)
        return render(request, 'livre/commande.html', {'form': form})


@user_passes_test(permissions.is_staff)
def voir_commandes(request, matricule=None):
    if request.method == 'GET':
        qs = models.Commande.objects.all()

        return render(
            request,
            'admin/liste_commandes.html',
            {
                'commandes': qs,
            }
        )
    else:
        Cm.objects.filter(pk=matricule).delete()
        return redirect('voir-commande')


# @user_passes_test(permissions.is_staff)
# def supprimer_commande(request, pk):
