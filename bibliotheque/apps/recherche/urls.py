from django.urls import path
from . import views

app_name = 'recherche'

urlpatterns = [
    path('',     views.recherche,       name='recherche'),
    path('ajax/',views.recherche_ajax,  name='ajax'),
]