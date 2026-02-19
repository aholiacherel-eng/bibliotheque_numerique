from django.urls import path
from . import views

app_name = 'lecture'

urlpatterns = [
    path('<slug:slug>/',                views.lire_livre,           name='lire_livre'),
    path('<slug:slug>/favori/',         views.toggle_favori,        name='toggle_favori'),
    path('<slug:slug>/progression/',    views.maj_progression,      name='maj_progression'),
    path('<slug:slug>/signets/',        views.liste_signets,        name='liste_signets'),
    path('<slug:slug>/signets/ajouter/',views.ajouter_signet,       name='ajouter_signet'),
    path('signets/<int:pk>/supprimer/', views.supprimer_signet,     name='supprimer_signet'),
]