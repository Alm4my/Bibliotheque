import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import now

from comptes import permissions
from livres import forms, models
from livres.models import Commande as Cm
from util import messages as m


# verification du statut de l'utilisateur en
# tant que staff i.e. bibliothécaire
@user_passes_test(permissions.is_staff)
def add_author(request):
    # creation d'un formulaire d'ajout de livre avec le contenu POST de la requête s'il
    # existe ou avec rien si non
    form = forms.AddAuthorForm(request.POST or None)

    # si notre requête est GET, nous retournons simplement le formulaire
    if request.method == 'GET':
        return render(request, 'auteur/creation.html', {'form': form})

    # si non, on vérifie si notre formulaire est valide et on l'enregistre.
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


# ici on vérifie si l'utilisateur fait partie du staff manuellement au lieu d'utiliser
# un décorateur.
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

    livres = models.Livre.objects.filter(nombre_de_copies__gte=1)
    if request.method == 'GET':
        return render(request, 'livre/commande.html', {'form': form, 'livres': livres})

    else:
        com = models.Commande.objects.filter(matricule=request.user.matricule).first()
        isbn = request.POST.get('isbn_livre')
        if com is None or not com.emprunt_en_cours:
            if form.is_valid():
                commande = form.save(commit=False)
                commande.isbn_livre_id = isbn
                livre = models.Livre.objects.filter(isbn=isbn).update(
                    nombre_de_copies=F('nombre_de_copies') - 1
                )
                # livre.nombre_de_copies -= 1
                # livre.save()
                commande.matricule = request.user
                commande.date_debut = now()
                commande.date_fin = now() + datetime.timedelta(days=4)
                commande.emprunt_en_cours = True
                commande.save()
                messages.success(request, m.COMMANDE_CREATION_SUCCESS)
                return redirect(reverse('home'))

        messages.error(request, m.COMMANDE_CREATION_ERROR)
        return render(request, 'livre/commande.html', {'form': form, 'livres': livres})


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
        commande = Cm.objects.filter(pk=matricule).first()
        models.Livre.objects.filter(isbn=commande.isbn_livre_id).update(
            nombre_de_copies=F('nombre_de_copies') + 1
        )
        commande.delete()
        return redirect('voir-commande')

# @user_passes_test(permissions.is_staff)
# def supprimer_commande(request, pk):
