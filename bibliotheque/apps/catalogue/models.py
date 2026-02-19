from django.db import models
from django.db.models import Avg
from django.utils.text import slugify


class Langue(models.Model):
    nom  = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nom


class Categorie(models.Model):
    nom         = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icone       = models.CharField(max_length=50, blank=True)
    parent      = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sous_categories'
    )

    class Meta:
        verbose_name         = 'Catégorie'
        verbose_name_plural  = 'Catégories'
        ordering             = ['nom']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Auteur(models.Model):
    prenom        = models.CharField(max_length=100)
    nom           = models.CharField(max_length=100)
    slug          = models.SlugField(unique=True, blank=True, max_length=250)
    biographie    = models.TextField(blank=True)
    photo         = models.ImageField(upload_to='auteurs/', blank=True, null=True)
    date_naissance = models.DateField(null=True, blank=True)
    date_deces    = models.DateField(null=True, blank=True)
    nationalite   = models.CharField(max_length=100, blank=True)
    site_web      = models.URLField(blank=True)

    class Meta:
        verbose_name         = 'Auteur'
        verbose_name_plural  = 'Auteurs'
        ordering             = ['nom', 'prenom']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.prenom}-{self.nom}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class Editeur(models.Model):
    nom      = models.CharField(max_length=200)
    adresse  = models.TextField(blank=True)
    site_web = models.URLField(blank=True)

    class Meta:
        verbose_name         = 'Éditeur'
        verbose_name_plural  = 'Éditeurs'

    def __str__(self):
        return self.nom


class Livre(models.Model):
    FORMAT_CHOICES = [
        ('pdf',  'PDF'),
        ('epub', 'ePub'),
        ('mobi', 'Mobi'),
    ]
    STATUT_CHOICES = [
        ('publie',   'Publié'),
        ('brouillon','Brouillon'),
        ('archive',  'Archivé'),
    ]

    # Informations principales
    titre              = models.CharField(max_length=300)
    slug               = models.SlugField(unique=True, blank=True, max_length=350)
    sous_titre         = models.CharField(max_length=300, blank=True)
    description        = models.TextField()
    isbn               = models.CharField(max_length=20, unique=True, blank=True, null=True)

    # Relations
    auteurs    = models.ManyToManyField(Auteur,   related_name='livres')
    editeur    = models.ForeignKey(Editeur,   on_delete=models.SET_NULL, null=True, blank=True, related_name='livres')
    categories = models.ManyToManyField(Categorie, related_name='livres')
    langue     = models.ForeignKey(Langue,    on_delete=models.SET_NULL, null=True, blank=True)

    # Fichiers
    couverture    = models.ImageField(upload_to='couvertures/', blank=True, null=True)
    fichier       = models.FileField(upload_to='livres/')
    format        = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    taille_fichier = models.PositiveIntegerField(null=True, blank=True, help_text="Taille en Ko")

    # Métadonnées
    date_publication  = models.DateField(null=True, blank=True)
    nombre_pages      = models.PositiveIntegerField(null=True, blank=True)
    statut            = models.CharField(max_length=20, choices=STATUT_CHOICES, default='publie')

    # Timestamps
    date_ajout        = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    # Compteurs
    nombre_telechargements = models.PositiveIntegerField(default=0)
    nombre_lectures        = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name         = 'Livre'
        verbose_name_plural  = 'Livres'
        ordering             = ['-date_ajout']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    @property
    def note_moyenne(self):
        result = self.avis.filter(valide=True).aggregate(Avg('note'))
        if result['note__avg']:
            return round(result['note__avg'], 1)
        return None

    @property
    def auteurs_str(self):
        return ', '.join(a.nom_complet for a in self.auteurs.all())


class Avis(models.Model):
    livre        = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='avis')
    utilisateur  = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='avis')
    note         = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire  = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    valide        = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Avis'
        verbose_name_plural = 'Avis'
        unique_together     = ('livre', 'utilisateur')
        ordering            = ['-date_creation']

    def __str__(self):
        return f"{self.utilisateur} → {self.livre} ({self.note}/5)"