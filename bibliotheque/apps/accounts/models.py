from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Utilisateur personnalisé avec rôle et informations complémentaires."""

    ROLE_CHOICES = [
        ('lecteur',        'Lecteur'),
        ('bibliothecaire', 'Bibliothécaire'),
        ('admin',          'Administrateur'),
    ]

    role             = models.CharField(max_length=20, choices=ROLE_CHOICES, default='lecteur')
    avatar           = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio              = models.TextField(blank=True)
    date_naissance   = models.DateField(null=True, blank=True)
    langue_preferee  = models.CharField(max_length=10, default='fr')
    notif_email      = models.BooleanField(default=True)

    class Meta:
        verbose_name         = 'Utilisateur'
        verbose_name_plural  = 'Utilisateurs'

    def __str__(self):
        return f"{self.username} [{self.get_role_display()}]"

    @property
    def is_bibliothecaire(self):
        return self.role in ('bibliothecaire', 'admin')