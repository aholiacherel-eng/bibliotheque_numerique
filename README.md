# BiblioNumérique

Bibliothèque numérique web construite avec Django. Permet de consulter, rechercher et lire des livres en PDF et ePub directement dans le navigateur.

## Stack

- **Back-end** — Django 5, PostgreSQL, Django REST Framework
- **Front-end** — Tailwind CSS (CDN), PDF.js, ePub.js
- **Auth** — Modèle User personnalisé avec rôles

## Fonctionnalités

- Catalogue de livres avec filtres par catégorie, format et tri
- Fiches auteurs et catégories
- Lecteur intégré PDF et ePub avec suivi de progression
- Système de favoris et signets
- Recherche full-text avec suggestions AJAX
- Tableau de bord utilisateur (progression, historique, favoris)
- Notation et avis sur les livres
- Interface d'administration Django

## Structure

```
bibliotheque/
├── apps/
│   ├── accounts/     # Utilisateurs, profils, dashboard
│   ├── catalogue/    # Livres, auteurs, catégories, avis
│   ├── lecture/      # Lecteur, favoris, signets, historique
│   └── recherche/    # Recherche full-text + AJAX
├── templates/        # HTML avec Tailwind CSS
├── static/           # JS, CSS

```

## Vu

<img width="1325" height="648" alt="biblionum2" src="https://github.com/user-attachments/assets/2d922ba1-ac85-4ab7-9407-7ba6495f1c87" />
<img width="1331" height="635" alt="biblionum1" src="https://github.com/user-attachments/assets/10ff149d-24c5-46db-9b9d-07812eaf9eb1" />
<img width="1294" height="589" alt="biblionum3" src="https://github.com/user-attachments/assets/e9a46751-6f59-42e2-b993-e27543829aa8" />

---

*Projet personnel — Développé avec Django & Tailwind CSS*
