from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('inscription/',            views.inscription,          name='inscription'),
    path('connexion/',              auth_views.LoginView.as_view(template_name='accounts/connexion.html'),  name='connexion'),
    path('deconnexion/',            auth_views.LogoutView.as_view(), name='deconnexion'),
    path('profil/',                 views.profil,               name='profil'),
    path('profil/modifier/',        views.modifier_profil,      name='modifier_profil'),
    path('tableau-de-bord/',        views.tableau_de_bord,      name='tableau_de_bord'),
]