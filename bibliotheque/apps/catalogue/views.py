from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Livre, Auteur, Categorie, Avis


def accueil(request):
    """Page d'accueil : livres récents, populaires, catégories."""
    livres_recents   = Livre.objects.filter(statut='publie').order_by('-date_ajout')[:8]
    livres_populaires = Livre.objects.filter(statut='publie').order_by('-nombre_lectures')[:8]
    categories       = Categorie.objects.filter(parent=None)[:6]

    return render(request, 'catalogue/accueil.html', {
        'livres_recents':    livres_recents,
        'livres_populaires': livres_populaires,
        'categories':        categories,
    })


def liste_livres(request):
    """Catalogue complet avec filtres basiques."""
    livres = Livre.objects.filter(statut='publie').prefetch_related('auteurs', 'categories')

    # Filtre par catégorie
    categorie_slug = request.GET.get('categorie')
    if categorie_slug:
        livres = livres.filter(categories__slug=categorie_slug)

    # Filtre par format
    format_filtre = request.GET.get('format')
    if format_filtre:
        livres = livres.filter(format=format_filtre)

    # Tri
    tri = request.GET.get('tri', '-date_ajout')
    if tri in ('-date_ajout', '-nombre_lectures', 'titre', '-date_publication'):
        livres = livres.order_by(tri)

    # Pagination
    paginator = Paginator(livres, 20)
    page      = request.GET.get('page', 1)
    livres_page = paginator.get_page(page)

    categories = Categorie.objects.all()

    return render(request, 'catalogue/liste_livres.html', {
        'livres':     livres_page,
        'categories': categories,
    })


def detail_livre(request, slug):
    """Fiche détaillée d'un livre."""
    livre = get_object_or_404(Livre, slug=slug, statut='publie')

    # Incrémenter le compteur de vues
    Livre.objects.filter(pk=livre.pk).update(nombre_lectures=livre.nombre_lectures + 1)

    avis = livre.avis.filter(valide=True).select_related('utilisateur')
    livres_similaires = Livre.objects.filter(
        categories__in=livre.categories.all(), statut='publie'
    ).exclude(pk=livre.pk).distinct()[:4]

    # Vérifier si l'utilisateur a déjà mis en favori
    en_favori = False
    if request.user.is_authenticated:
        from apps.lecture.models import Favori
        en_favori = Favori.objects.filter(utilisateur=request.user, livre=livre).exists()

    return render(request, 'catalogue/detail_livre.html', {
        'livre':            livre,
        'avis':             avis,
        'livres_similaires': livres_similaires,
        'en_favori':        en_favori,
    })


def liste_categories(request):
    categories = Categorie.objects.filter(parent=None).prefetch_related('sous_categories')
    return render(request, 'catalogue/liste_categories.html', {'categories': categories})


def livres_categorie(request, slug):
    categorie = get_object_or_404(Categorie, slug=slug)
    livres    = Livre.objects.filter(categories=categorie, statut='publie')
    paginator = Paginator(livres, 20)
    page      = request.GET.get('page', 1)
    return render(request, 'catalogue/livres_categorie.html', {
        'categorie': categorie,
        'livres':    paginator.get_page(page),
    })


def liste_auteurs(request):
    auteurs = Auteur.objects.all().order_by('nom')
    return render(request, 'catalogue/liste_auteurs.html', {'auteurs': auteurs})


def detail_auteur(request, slug):
    auteur = get_object_or_404(Auteur, slug=slug)
    livres = auteur.livres.filter(statut='publie')
    return render(request, 'catalogue/detail_auteur.html', {
        'auteur': auteur,
        'livres': livres,
    })


@login_required
def ajouter_avis(request, slug):
    """Soumettre un avis sur un livre."""
    livre = get_object_or_404(Livre, slug=slug, statut='publie')

    if request.method == 'POST':
        note        = request.POST.get('note')
        commentaire = request.POST.get('commentaire', '')

        if note and note.isdigit() and 1 <= int(note) <= 5:
            Avis.objects.update_or_create(
                livre=livre,
                utilisateur=request.user,
                defaults={'note': int(note), 'commentaire': commentaire}
            )
            messages.success(request, "Votre avis a été enregistré.")
        else:
            messages.error(request, "Note invalide.")

    return redirect('catalogue:detail_livre', slug=slug)