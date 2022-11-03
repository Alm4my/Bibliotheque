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
    )

]
