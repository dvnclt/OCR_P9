from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from Content.models import Post, Review
from .models import Follow


# Vue de page d'accueil de l'utilisateur
@login_required
def home(request):
    # Récupère tous les posts et reviews
    posts = Post.objects.all()
    reviews = Review.objects.all()

    return render(request, 'home.html', {
        'posts': posts,
        'reviews': reviews,
    })


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
