# Gère la logique des abonnements et des suivis des membres
# Ainsi que la recherche de membres.

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import Member, Subscription


class SubscriptionView(View):
    template_name = 'subscription.html'

    # Gère la récupération des abonnements, des abonnés et des résultats de
    # recherche de membres.
    def get(self, request):
        # Récupère la liste des utilisateurs suivis par un utilisateur donné
        following = Subscription.objects.filter(
            follower=request.user
            # Trie par ordre alphabétique
            ).order_by('following__username')
        # Extrait les IDs des users suivis pour vérification dans le template
        following_ids = following.values_list('following_id', flat=True)
        # Récupère la liste des utilisateurs qui suivent un utilisateur donné
        followers = Subscription.objects.filter(
            following=request.user
            # Trie par ordre alphabétique
            ).order_by('follower__username')

        # Récupère le terme de recherche pour rechercher des membres.
        query = request.GET.get('q', '')
        # Initialise une requête vide
        members = Member.objects.none()

        if query:
            # Cherche des membres dont le nom contient la requête.
            members = Member.objects.filter(
                username__icontains=query
                # Exclut l'utilisateur donné de la recherche + trie
                ).exclude(id=request.user.id).order_by('username')

        # Rend la page avec la liste des abonnements, des abonnés
        # et des membres trouvés.
        return render(request, self.template_name, {
            'following': following,
            'followers': followers,
            'members': members,
            'query': query,
            'following_ids': following_ids,
        })

    # Gère les actions de suivi et de désabonnement des membres via des
    # requêtes POST.
    def post(self, request, *args, **kwargs):
        # Récupère l'ID du membre à suivre/désabonner depuis le formulaire.
        member_id = request.POST.get('member_id')
        if 'follow' in request.POST and member_id:
            # Cherche le membre à suivre
            # Renvoie une erreur 404 si introuvable.
            following = get_object_or_404(Member, id=member_id)
            # S'assure que l'utilisateur ne s'abonne pas à lui-même
            if following != request.user:
                Subscription.objects.get_or_create(
                    follower=request.user, following=following
                )
        elif 'unfollow' in request.POST and member_id:
            # Logique pour se désabonner d'un membre
            following = get_object_or_404(Member, id=member_id)
            Subscription.objects.filter(
                    follower=request.user, following=following
                    ).delete()

        return redirect('subscription')
