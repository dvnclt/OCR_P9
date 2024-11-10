# Définition des modèles pour l'application Accounts :
# 1. Modèle Member pour les utilisateurs personnalisés.
# 2. Modèle Subscription pour gérer les abonnements entre utilisateurs.

from django.db import models
from django.contrib.auth.models import AbstractUser


# Déclare un modèle personnalisé "Member" en étendant AbstractUser pour
# ajouter des champs personnalisés.
class Member(AbstractUser):
    # Méthode pour afficher une représentation lisible de l'utilisateur.
    def __str__(self):
        return (f"{self.username} - {self.email}\n"
                f"{self.first_name} - {self.last_name}")


# Déclare un modèle "Subscription" pour gérer les abonnements entre membres.
class Subscription(models.Model):
    # Champ pour représenter l'utilisateur qui est suivi
    # (relation inverse avec 'followers').
    following = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='followers'
    )
    # Champ pour représenter l'utilisateur qui suit
    # (relation inverse avec 'following').
    follower = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='following'
    )
    # Enregistre la date et l'heure de la création de l'abonnement.
    created_at = models.DateTimeField(auto_now_add=True)

    # Méthode pour afficher une représentation lisible de l'abonnement.
    def __str__(self):
        return f"{self.follower} suit {self.following}"
