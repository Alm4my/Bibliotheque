from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from comptes.forms import CreateUserForm, LoginForm
from util.error_messages import FAILED_REGISTRATION, WRONG_CREDENTIALS


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
            return redirect('home')

        messages.error(req, WRONG_CREDENTIALS)
        return render(
            req,
            'comptes/login.html',
            {
                'form': form
            }
        )
