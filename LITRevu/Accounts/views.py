from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import Member, Subscription


class SubscriptionView(View):
    template_name = 'subscription.html'

    def get(self, request):
        # Récupère la liste des utilisateurs suivis par un utilisateur donné
        following = Subscription.objects.filter(follower=request.user)
        following_ids = following.values_list('following_id', flat=True)
        # Récupère la liste des utilisateurs qui suivent un utilisateur donné
        followers = Subscription.objects.filter(following=request.user)

        # Gestion de la recherche
        query = request.GET.get('q', '')
        members = Member.objects.none()

        if query:
            members = Member.objects.filter(username__icontains=query)

        return render(request, self.template_name, {
            'following': following,
            'followers': followers,
            'members': members,
            'query': query,
            'following_ids': following_ids,
        })

    def post(self, request, *args, **kwargs):
        member_id = request.POST.get('member_id')
        if 'follow' in request.POST and member_id:
            # Logique pour suivre un membre
            following = get_object_or_404(Member, id=member_id)
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
