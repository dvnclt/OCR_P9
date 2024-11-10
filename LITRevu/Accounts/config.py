# Adapte les modèles par défaut de Django aux modèles personnalisés

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# Récupère le modèle d'utilisateur personnalisé défini dans le projet.
User = get_user_model()


# Adapte la classe UserCreationForm
class MemberCreationForm(UserCreationForm):
    class Meta:
        # Associe le formulaire au modèle d'utilisateur personnalisé.
        model = User
        # Détermine les champs à inclure dans le formulaire
        fields = ('username', 'password1', 'password2')
