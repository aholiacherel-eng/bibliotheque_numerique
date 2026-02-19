from django.db import models


class Favori(models.Model):
    utilisateur = models.ForeignKey('accounts.User',   on_delete=models.CASCADE, related_name='favoris')
    livre       = models.ForeignKey('catalogue.Livre', on_delete=models.CASCADE, related_name='mis_en_favoris')
    date_ajout  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together     = ('utilisateur', 'livre')
        verbose_name        = 'Favori'
        verbose_name_plural = 'Favoris'
        ordering            = ['-date_ajout']

    def __str__(self):
        return f"{self.utilisateur} ❤ {self.livre}"


class Progression(models.Model):
    """Avancement de lecture d'un utilisateur sur un livre."""
    utilisateur    = models.ForeignKey('accounts.User',   on_delete=models.CASCADE, related_name='progressions')
    livre          = models.ForeignKey('catalogue.Livre', on_delete=models.CASCADE, related_name='progressions')
    page_courante  = models.PositiveIntegerField(default=1)
    pourcentage    = models.FloatField(default=0.0)
    derniere_lecture = models.DateTimeField(auto_now=True)
    termine        = models.BooleanField(default=False)
    date_debut     = models.DateTimeField(auto_now_add=True)
    date_fin       = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together     = ('utilisateur', 'livre')
        verbose_name        = 'Progression'
        verbose_name_plural = 'Progressions'

    def save(self, *args, **kwargs):
        if self.livre.nombre_pages:
            self.pourcentage = min((self.page_courante / self.livre.nombre_pages) * 100, 100.0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.utilisateur} — {self.livre} ({self.pourcentage:.0f}%)"


class Signet(models.Model):
    utilisateur  = models.ForeignKey('accounts.User',   on_delete=models.CASCADE, related_name='signets')
    livre        = models.ForeignKey('catalogue.Livre', on_delete=models.CASCADE, related_name='signets')
    page         = models.PositiveIntegerField()
    titre        = models.CharField(max_length=200, blank=True)
    note         = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering            = ['page']
        verbose_name        = 'Signet'
        verbose_name_plural = 'Signets'

    def __str__(self):
        return f"p.{self.page} — {self.livre} ({self.utilisateur})"


class HistoriqueLecture(models.Model):
    utilisateur  = models.ForeignKey('accounts.User',   on_delete=models.CASCADE, related_name='historique')
    livre        = models.ForeignKey('catalogue.Livre', on_delete=models.CASCADE, related_name='historique')
    date_debut   = models.DateTimeField(auto_now_add=True)
    date_fin     = models.DateTimeField(null=True, blank=True)
    duree_minutes = models.PositiveIntegerField(default=0)
    pages_lues   = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name        = 'Session de lecture'
        verbose_name_plural = 'Sessions de lecture'
        ordering            = ['-date_debut']

    def __str__(self):
        return f"{self.utilisateur} — {self.livre} — {self.date_debut:%d/%m/%Y}"


class ListeLecture(models.Model):
    utilisateur    = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='listes_lecture')
    nom            = models.CharField(max_length=200, default='Ma liste')
    description    = models.TextField(blank=True)
    publique       = models.BooleanField(default=False)
    livres         = models.ManyToManyField('catalogue.Livre', through='LivreDansListe', related_name='listes')
    date_creation  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Liste de lecture'
        verbose_name_plural = 'Listes de lecture'

    def __str__(self):
        return f"{self.nom} ({self.utilisateur})"


class LivreDansListe(models.Model):
    liste           = models.ForeignKey(ListeLecture,       on_delete=models.CASCADE)
    livre           = models.ForeignKey('catalogue.Livre',  on_delete=models.CASCADE)
    ordre           = models.PositiveSmallIntegerField(default=0)
    note_personnelle = models.TextField(blank=True)
    date_ajout      = models.DateTimeField(auto_now_add=True)
    lu              = models.BooleanField(default=False)

    class Meta:
        ordering        = ['ordre']
        unique_together = ('liste', 'livre')