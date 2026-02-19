from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
    path('',                            views.accueil,          name='accueil'),
    path('livres/',                     views.liste_livres,     name='liste_livres'),
    path('livres/<slug:slug>/',         views.detail_livre,     name='detail_livre'),
    path('categories/',                 views.liste_categories, name='liste_categories'),
    path('categories/<slug:slug>/',     views.livres_categorie, name='livres_categorie'),
    path('auteurs/',                    views.liste_auteurs,    name='liste_auteurs'),
    path('auteurs/<slug:slug>/',        views.detail_auteur,    name='detail_auteur'),
    path('livres/<slug:slug>/avis/',    views.ajouter_avis,     name='ajouter_avis'),
]