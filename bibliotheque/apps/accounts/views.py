from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ProfilForm


def inscription(request):
    """Inscription d'un nouvel utilisateur."""
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username} ! Votre compte est créé.")
            return redirect('catalogue:accueil')
    else:
        form = InscriptionForm()
    return render(request, 'accounts/inscription.html', {'form': form})


@login_required
def profil(request):
    """Page de profil de l'utilisateur connecté."""
    return render(request, 'accounts/profil.html', {'utilisateur': request.user})


@login_required
def modifier_profil(request):
    """Modification du profil."""
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('accounts:profil')
    else:
        form = ProfilForm(instance=request.user)
    return render(request, 'accounts/modifier_profil.html', {'form': form})


@login_required
def tableau_de_bord(request):
    """Tableau de bord personnel : progression, favoris, historique."""
    from apps.lecture.models import Progression, Favori, HistoriqueLecture
    progressions = Progression.objects.filter(utilisateur=request.user).select_related('livre')[:5]
    favoris      = Favori.objects.filter(utilisateur=request.user).select_related('livre')[:5]
    historique   = HistoriqueLecture.objects.filter(utilisateur=request.user).select_related('livre')[:10]

    return render(request, 'accounts/tableau_de_bord.html', {
        'progressions': progressions,
        'favoris':      favoris,
        'historique':   historique,
    })