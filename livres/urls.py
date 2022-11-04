from django.urls import path

from livres import views

urlpatterns = [
    path('auteur/', views.add_author, name="author-create"),
    path('ajouter/', views.add_book, name="book-create"),
    path('commande/', views.add_commande, name="commande"),
    path('commande/voir/', views.voir_commandes, name="voir-commande"),
    path('commande/voir/<str:matricule>/', views.voir_commandes, name="voir-commande"),
]
