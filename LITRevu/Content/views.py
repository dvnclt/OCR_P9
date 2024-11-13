from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import Post, Review
from .forms import PostReviewForm, ReviewForm

from Accounts.models import Subscription


# Vue pour la création d'un post
class PostCreateView(CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('feed')

    # Assigne l'utilisateur comme auteur du post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Vue pour la modification d'un post
class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('my_posts')

    # Restreint l'accès au créateur du post
    def test_func(self):
        return self.request.user == self.get_object().author

    # S'assure que l'utilisateur ne peut modifier que ses propres posts
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


# Vue pour la suppression d'un post
class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('my_posts')

    # Restreint l'accès au créateur du post
    def test_func(self):
        return self.request.user == self.get_object().author

    # S'assure que l'utilisateur ne peut supprimer que ses propres posts
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = 'post'
        return context


# Vue pour l'ajout d'une review à un post existant
class ReviewCreateView(CreateView):
    model = Review
    template_name = 'review_form.html'
    form_class = ReviewForm
    success_url = reverse_lazy('feed')

    # Assigne l'utilisateur comme auteur de la review
    def form_valid(self, form):
        form.instance.author = self.request.user

        # Récupérer le post_id à partir de la requête GET
        post_id = self.request.GET.get('post_id')
        if post_id:
            post = get_object_or_404(Post, id=post_id)

            # Vérifie si l'utilisateur a déjà publié une critique pour ce post
            if Review.objects.filter(post=post).exists():
                messages.error(
                    self.request, "Erreur: Une critique existe déjà "
                                  "pour ce post."
                )
                return HttpResponseRedirect(reverse('feed'))

            # Associe la critique au post
            form.instance.post = post

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupère le post à partir de l'ID passé dans la requête
        post_id = self.request.GET.get('post_id')
        if post_id:
            post = get_object_or_404(Post, id=post_id)
            context['post'] = post  # Passe le post au template

        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Modifie les labels des champs
        form.fields['title'].label = 'Titre'
        form.fields['rating'].label = 'Note'
        form.fields['content'].label = 'Commentaire'

        return form


# Vue pour la modification d'une review
class ReviewUpdateView(UserPassesTestMixin, UpdateView):
    model = Review
    template_name = 'review_form.html'
    form_class = ReviewForm
    success_url = reverse_lazy('my_posts')

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        return context


# Vue pour la suppression d'une review
class ReviewDeleteView(UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('my_posts')

    # Restreint l'accès au créateur de la review
    def test_func(self):
        return self.request.user == self.get_object().author

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = 'review'
        return context


# Vue pour la création d'une review en créant un post
class PostReviewCreateView(View):
    def get(self, request, *args, **kwargs):
        form = PostReviewForm()
        return render(request, 'post_review_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PostReviewForm(request.POST)

        if form.is_valid():
            # Créer et sauvegarder le post
            post = Post(
                title=form.cleaned_data['post_title'],
                content=form.cleaned_data['post_content'],
                author=request.user
            )
            post.save()

            # Créer et sauvegarder la critique
            review = Review(
                post=post,
                title=form.cleaned_data['review_title'],
                content=form.cleaned_data['review_content'],
                rating=form.cleaned_data['review_rating'],
                author=request.user
            )
            review.save()

            return redirect('feed')

        return render(request, 'post_review_form.html', {'form': form})


# Vue pour la gestion de l'affichage du flux
class FeedView(View):
    template_name = 'feed.html'

    def get(self, request, *args, **kwargs):

        # Récupère la liste des utilisateurs suivis
        followed_users = Subscription.objects.filter(
            follower=request.user).values_list('following', flat=True)

        # Récupère les posts et les critiques
        # des utilisateurs suivis et de l'utilisateur donné
        posts = Post.objects.filter(
            Q(author__id__in=followed_users) |
            Q(author=request.user)
            ).order_by('-created_at')
        reviews = Review.objects.filter(
            Q(author__id__in=followed_users) |
            Q(author=request.user)
            ).order_by('-created_at')

        # Récupère également les reviews en rapport avec les posts du user
        my_post_reviews = Review.objects.filter(
            post__author=request.user
            ).order_by('-created_at')

        # Ajout des attributs pour éviter 'item.item' dans le template
        items = []
        for post in posts:

            # Vérifie si une review a déjà été ajoutée pour le post donné
            has_reviewed = Review.objects.filter(post=post).exists()

            items.append({
                'type': 'post',
                'author': post.author,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'image': post.image,
                'id': post.id,
                'has_reviewed': has_reviewed
            })
        for review in list(reviews) + list(my_post_reviews):
            items.append({
                'type': 'review',
                'author': review.author,
                'title': review.title,
                'content': review.content,
                'created_at': review.created_at,
                'rating': review.rating,
                'post': review.post,
                'stars_display': review.stars_display(),
                'id': review.id
            })

        # Trie les éléments par date de création
        sorted_items = sorted(
            items, key=lambda x: x['created_at'], reverse=True)

        return render(request, 'feed.html', {'sorted_items': sorted_items})


class MyPostsView(View):
    template_name = 'my_posts.html'

    def get(self, request, *args, **kwargs):
        # Récupère l'utilisateur à partir de l'URL ou de la requête
        user = request.user

        # Récupère tous les posts et critiques publiés par cet utilisateur
        posts = Post.objects.filter(author=user).order_by('-created_at')
        reviews = Review.objects.filter(author=user).order_by('-created_at')

        # Ajout des attributs pour éviter 'item.item' dans le template
        items = []
        for post in posts:
            items.append({
                'type': 'post',
                'author': post.author,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'image': post.image,
                'id': post.id,
            })
        for review in reviews:
            items.append({
                'type': 'review',
                'author': review.author,
                'title': review.title,
                'content': review.content,
                'created_at': review.created_at,
                'rating': review.rating,
                'post': review.post,
                'stars_display': review.stars_display(),
                'id': review.id
            })

        # Trie les éléments par date de création
        sorted_items = sorted(
            items, key=lambda x: x['created_at'], reverse=True)

        return render(request, 'my_posts.html', {'sorted_items': sorted_items})
