import re

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render

from comptes import permissions
from comptes.forms import CreateBiblioForm, CreateUserForm, LoginForm
from comptes.models import Utilisateur
from util.messages import (
    BIB_CREATE_FAIL, BIB_CREATE_SUCCESS, FAILED_REGISTRATION,
    PASSWD_CHANGE_FAIL, PASSWD_CHANGE_SUCCESS, WRONG_CREDENTIALS,
)


def register_view(req):
    form = CreateUserForm(req.POST or None)
    if req.method == "GET":
        return render(req, "comptes/inscription.html", {'register_form': form})
    else:
        if form.is_valid():
            user = form.save()
            login(req, user, backend='comptes.backends.AuthBackend')
            messages.success(req, "Inscription Réussie!")
            return redirect('home')
        messages.error(req, FAILED_REGISTRATION)

    return render(req, "comptes/inscription.html", {"register_form": form})


def login_view(req):
    form = LoginForm(req.POST)

    if req.method == 'GET':
        return render(req, 'comptes/login.html', {'form': form})

    else:
        if req.POST and form.is_valid() and form.login(req):
            return redirect(req.GET.get('next')) \
                if req.GET.get('next') else redirect('home')

        messages.error(req, WRONG_CREDENTIALS)
        return render(
            req,
            'comptes/login.html',
            {
                'form': form
            }
        )


@user_passes_test(permissions.is_staff)
def register_bib(request):
    form = CreateBiblioForm(request.POST or None)
    if request.method == 'GET':
        return render(request, 'admin/ajout_staff.html', {'form': form})

    else:
        if form.is_valid():
            form.save()
            messages.success(request, BIB_CREATE_SUCCESS)
            return redirect('home')

        messages.error(request, BIB_CREATE_FAIL)
        return render(request, 'admin/ajout_staff.html', {'form': form})


@user_passes_test(permissions.is_staff)
def change_user_password(request):
    utilisateurs = Utilisateur.objects.all()

    if request.method == 'GET':
        return render(request, 'admin/modifier_mdp.html', {'utilisateurs': utilisateurs})

    else:
        regex = r'^(?=.*\d)[A-Za-z\d]{8,}$'
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password2 == password1 and re.match(regex, password1):
            user = Utilisateur.objects.filter(pk=request.POST.get('pk')).first()
            if user:
                user.set_password(password1)
                messages.success(request, PASSWD_CHANGE_SUCCESS)
                user.save()
                return redirect('home')

        messages.error(request, PASSWD_CHANGE_FAIL)
        return render(request, 'admin/modifier_mdp.html', {'utilisateurs': utilisateurs})

