# LITRevu

LITRevu est une application web permettant aux membres de publier et de demander des critiques de livres ou d'articles. Le site encourage la découverte de nouvelles lectures à travers des critiques partagées par les membres.

## Table des matières

- [Versions](#versions)
- [Installation](#installation)
- [Configuration](#configuration)
- [Fonctionnalités](#fonctionnalités)
- [Composants principaux](#composants-principaux)

---

## Versions

- Python 3.12.2
- Django 5.1.2

---

## Installation

1. **Cloner le dépôt**
```
   git clone <URL_DU_DEPOT>
   cd LITRevu
```

2. **Créer un environnement virtuel**
```
python3 -m venv env
source env/bin/activate  # Sur Linux/macOS
env\Scripts\activate.bat # Sur Windows
```

3. **Installer les dépendances**
```
pip install -r requirements.txt
```

4. **Exécuter les migrations**
```
python manage.py migrate
```

5. **Créer un superutilisateur**
```
python manage.py createsuperuser

```

6. **Lancer le serveur local**
```
python manage.py runserver
```

L'application est maintenant accessible à l'adresse http://127.0.0.1:8000.

---

## Configuration

**Paramètres de la timezone**
Dans settings.py, la timezone est définie sur 'Europe/Paris'.

**Paramètres de la timezone**
Le language_code est défini à 'fr-FR'.

**Répertoires de templates**
Les templates sont configurés pour être accessibles depuis le répertoire racine du projet. DIRS dans la configuration des templates est ainsi défini : 
```
'DIRS': [BASE_DIR/"LITRevu"/"templates"],
```

**Téléversement d'images**
Le modèle Post permet le téléversement d’images. Les images sont stockées localement dans le répertoire media/post_images.

---

## Fonctionnalités

**Application principale LITRevu**

**Settings.py** : fichier de configuration de l'application
**urls.py** : fichier de configuration des urls de l'application
**media/post_images** : dossier pour stocker les images des tickets

**Application Content**

**Billets et Critiques** : Les membres peuvent publier des billets demandant des critiques et répondre à un billet en postant une critique.
Ils peuvent également posté un billet et une critique à ce billet dans un même temps.

**Affichage des Critiques** : Les billets et critiques sont affichés avec l’auteur, la date de création et un aperçu du contenu.

**Gestion des billets et critiques** : Les membres peuvent modifier ou supprimer leurs propres billets et critiques. Les suppressions s’effectuent via une méthode POST et dépendent d'une confirmation.


**Application Accounts**

**Authentification** : Utilisation de l'AuthenticationForm de Django sans personnalisation des contraintes pour la connexion.

**Système de suivi** : Les membres peuvent suivre d’autres membres via un modèle Follow.

**Déconnexion** : La déconnexion redirige les membres vers la page de connexion grâce à une redirection (settings.py).

**Accessibilité et Conformité WCAG**
Toutes les pages visibles par les membres suivent les bonnes pratiques d’accessibilité du référentiel WCAG pour assurer une expérience inclusive.

---

## Composants principaux

1. **Application Accounts** :

**Modèles**

`class Member(AbstractUser):` Classe personnalisée reprenant la configuration par défaut de Django

`class Subscription(models.Model):` Modèle pour la gestion des abonnements entre membres

**Vues**

`class SubscriptionView(View):` Gère la logique des abonnements et désabonnements entre membres.

2. **Application Content** :

**Modèles**

`class Post(models.Model):` Contient le titre, le contenu, la date de création, l’auteur et un champ pour les images.

`class Review(models.Model):` Associé à Post, contient un titre, un contenu, une date de création et un auteur.

**Vues**

Gestion des différentes logique pour la création, la modification, la suppression et l'affichage des billets et critiques. Toutes les vues héritent directement des vues par défaut de Django (View, CreateView, UpdateView et DeleteView).

