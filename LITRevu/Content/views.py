from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

from itertools import chain

from .models import Post, Review
from .forms import PostReviewForm


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
    fields = ['title', 'content']
    success_url = reverse_lazy('feed')

    # Restreint l'accès au créateur du post
    def test_func(self):
        return self.request.user == self.get_object().author

    # TODO : Vérifier l'utilité
    # S'assure que l'utilisateur ne peut modifier que ses propres posts
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


# Vue pour la suppression d'un post
class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('feed')

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
    fields = ['title', 'content']
    success_url = reverse_lazy('feed')

    # Assigne l'utilisateur comme auteur de la review
    def form_valid(self, form):
        form.instance.author = self.request.user

        # Récupérer le post_id à partir de la requête GET
        post_id = self.request.GET.get('post_id')
        if post_id:
            # Associer la critique au post
            form.instance.post = Post.objects.get(id=post_id)

        return super().form_valid(form)


# Vue pour la modification d'une review
class ReviewUpdateView(UserPassesTestMixin, UpdateView):
    model = Review
    template_name = 'review_form.html'
    fields = ['post', 'title', 'content']
    success_url = reverse_lazy('feed')

    # Restreint l'accès au créateur de la review
    def test_func(self):
        return self.request.user == self.get_object().author

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)


# Vue pour la suppression d'une review
class ReviewDeleteView(UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('feed')

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
                author=request.user
            )
            review.save()

            return redirect('feed')

        return render(request, 'post_review_form.html', {'form': form})


# Vue pour la gestion de l'affichage du flux
class FeedView(View):
    template_name = 'feed.html'

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        reviews = Review.objects.all()

        sorted_items = sorted(
            chain(posts, reviews),
            key=lambda instance: instance.created_at,
            reverse=True
        )

        # Ajouter un type à chaque élément
        sorted_items_with_type = []
        for item in sorted_items:
            item_type = 'post' if isinstance(item, Post) else 'review'
            has_reviewed = None

            if item_type == 'post':
                has_reviewed = item.reviews.filter(
                    author=request.user
                    ).exists()

            sorted_items_with_type.append({
                'item': item,
                'type': item_type,
                'has_reviewed': has_reviewed,
            })

        context = {
            'sorted_items': sorted_items_with_type
        }

        return render(request, self.template_name, context)
