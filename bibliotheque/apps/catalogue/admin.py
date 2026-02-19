from django.contrib import admin
from .models import Livre, Auteur, Categorie, Editeur, Langue, Avis


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display   = ('titre', 'auteurs_str', 'format', 'statut', 'nombre_lectures', 'date_ajout')
    list_filter    = ('statut', 'format', 'categories', 'langue')
    search_fields  = ('titre', 'isbn', 'description')
    prepopulated_fields = {'slug': ('titre',)}
    filter_horizontal   = ('auteurs', 'categories')
    readonly_fields = ('nombre_telechargements', 'nombre_lectures', 'date_ajout', 'date_modification')


@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display  = ('nom_complet', 'nationalite')
    search_fields = ('nom', 'prenom')
    prepopulated_fields = {'slug': ('prenom', 'nom')}


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display  = ('nom', 'parent')
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('livre', 'utilisateur', 'note', 'valide', 'date_creation')
    list_filter  = ('valide', 'note')
    actions      = ['valider', 'invalider']

    def valider(self, request, queryset):
        queryset.update(valide=True)
    valider.short_description = "Valider les avis sélectionnés"

    def invalider(self, request, queryset):
        queryset.update(valide=False)
    invalider.short_description = "Invalider les avis sélectionnés"


admin.site.register(Editeur)
admin.site.register(Langue)