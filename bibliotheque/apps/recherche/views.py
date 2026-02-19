from django.shortcuts import render
from django.db.models import Q
from apps.catalogue.models import Livre, Auteur, Categorie


def recherche(request):
    """Recherche globale avec filtres."""
    q          = request.GET.get('q', '').strip()
    categorie  = request.GET.get('categorie', '')
    format_    = request.GET.get('format', '')
    langue     = request.GET.get('langue', '')
    tri        = request.GET.get('tri', '-date_ajout')

    livres = Livre.objects.filter(statut='publie').prefetch_related('auteurs', 'categories')

    if q:
        livres = livres.filter(
            Q(titre__icontains=q)        |
            Q(description__icontains=q)  |
            Q(auteurs__nom__icontains=q) |
            Q(auteurs__prenom__icontains=q) |
            Q(isbn__icontains=q)
        ).distinct()

    if categorie:
        livres = livres.filter(categories__slug=categorie)

    if format_:
        livres = livres.filter(format=format_)

    if langue:
        livres = livres.filter(langue__code=langue)

    if tri in ('-date_ajout', '-nombre_lectures', 'titre', '-date_publication'):
        livres = livres.order_by(tri)

    categories = Categorie.objects.all()

    return render(request, 'recherche/resultats.html', {
        'livres':    livres,
        'q':         q,
        'categories': categories,
        'total':     livres.count(),
    })


def recherche_ajax(request):
    """Suggestions de recherche en temps réel (appelé par JS)."""
    from django.http import JsonResponse
    q = request.GET.get('q', '').strip()

    if len(q) < 2:
        return JsonResponse({'suggestions': []})

    livres = Livre.objects.filter(
        Q(titre__icontains=q) | Q(auteurs__nom__icontains=q),
        statut='publie'
    ).distinct()[:8]

    suggestions = [{
        'id':    l.pk,
        'titre': l.titre,
        'auteurs': l.auteurs_str,
        'url':   f'/livres/{l.slug}/',
    } for l in livres]

    return JsonResponse({'suggestions': suggestions})