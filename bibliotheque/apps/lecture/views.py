from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from apps.catalogue.models import Livre
from .models import Favori, Progression, Signet, HistoriqueLecture


@login_required
def lire_livre(request, slug):
    """Page de lecture intégrée (PDF.js / epub.js)."""
    livre = get_object_or_404(Livre, slug=slug, statut='publie')

    # Récupérer ou créer la progression
    progression, _ = Progression.objects.get_or_create(
        utilisateur=request.user,
        livre=livre,
        defaults={'page_courante': 1}
    )

    # Créer une session de lecture
    HistoriqueLecture.objects.create(utilisateur=request.user, livre=livre)

    signets = Signet.objects.filter(utilisateur=request.user, livre=livre)

    return render(request, 'lecture/lire.html', {
        'livre':       livre,
        'progression': progression,
        'signets':     signets,
    })


@login_required
@require_POST
def toggle_favori(request, slug):
    """Ajouter/retirer un livre des favoris (appelé par JS)."""
    livre   = get_object_or_404(Livre, slug=slug)
    favori, created = Favori.objects.get_or_create(utilisateur=request.user, livre=livre)

    if not created:
        favori.delete()
        return JsonResponse({'statut': 'retire'})
    return JsonResponse({'statut': 'ajoute'})


@login_required
@require_POST
def maj_progression(request, slug):
    """Mettre à jour la progression de lecture (appelé par JS)."""
    livre = get_object_or_404(Livre, slug=slug)

    try:
        data         = json.loads(request.body)
        page_courante = int(data.get('page', 1))
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'erreur': 'Données invalides'}, status=400)

    progression, _ = Progression.objects.get_or_create(
        utilisateur=request.user, livre=livre
    )
    progression.page_courante = page_courante
    if livre.nombre_pages and page_courante >= livre.nombre_pages:
        progression.termine = True
    progression.save()

    return JsonResponse({
        'page':       progression.page_courante,
        'pourcentage': round(progression.pourcentage, 1),
        'termine':    progression.termine,
    })


@login_required
def liste_signets(request, slug):
    livre   = get_object_or_404(Livre, slug=slug)
    signets = Signet.objects.filter(utilisateur=request.user, livre=livre)
    return render(request, 'lecture/signets.html', {'livre': livre, 'signets': signets})


@login_required
@require_POST
def ajouter_signet(request, slug):
    livre = get_object_or_404(Livre, slug=slug)
    page  = request.POST.get('page')
    titre = request.POST.get('titre', '')
    note  = request.POST.get('note', '')

    if page and page.isdigit():
        Signet.objects.create(
            utilisateur=request.user,
            livre=livre,
            page=int(page),
            titre=titre,
            note=note,
        )
    return redirect('lecture:lire_livre', slug=slug)


@login_required
@require_POST
def supprimer_signet(request, pk):
    signet = get_object_or_404(Signet, pk=pk, utilisateur=request.user)
    slug   = signet.livre.slug
    signet.delete()
    return redirect('lecture:lire_livre', slug=slug)