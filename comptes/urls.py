from django.contrib.auth import views as auth_views
from django.urls import path

from comptes import views

urlpatterns = [

    path(
        'inscription/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='comptes/logout.html'),
        name='logout'
    ),

    path(
        'changer-mdp/',
        auth_views.PasswordChangeView.as_view(
            template_name='comptes/changer-mdp.html'
        ),
    ),

    path(
        'changer-mdp-termine/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='home.html'
        ),
        name='password_change_done'
    ),

    path(
        'reinit-mdp/',
        auth_views.PasswordResetView.as_view(
            template_name='comptes/reinit-pw.html'
        ), name='password_reset'
    ),

    path(
        'reinit-mdp-termine/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='comptes/message-reinit-envoye.html'
        ), name='password_reset_done'
    ),

    path(
        'reinit-mdp-confirm/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='comptes/mdp-confirm.html'
        ), name='password_reset_confirm'
    ),

    path(
        'reinit-mdp-confirm-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='comptes/mdp-confirm-complete.html'),
        name='password_reset_confirm'
    ),

    path('add-bib/', views.register_bib, name='register-bib'),

    path('change-user-mdp/', views.change_user_password, name='register-bib'),
    path('change-user-mdp/<str:pk>', views.change_user_password, name='register-bib'),
]
