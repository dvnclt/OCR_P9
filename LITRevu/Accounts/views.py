from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Follow


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def follow_list(request):
    # Récupère la liste des utilisateurs suivis par l'utilisateur donné
    follows = Follow.objects.filter(follower=request.user)
    # Récupère la liste des utilisateurs qui suivent l'utilisateur donné
    followers = Follow.objects.filter(followed=request.user)

    return render(request, 'follow.html', {
        'follows': follows,
        'followers': followers,
        })
