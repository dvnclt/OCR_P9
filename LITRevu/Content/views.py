from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from .models import Post, Review


# Vue pour l'affichage du détail d'un post
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(post=self.object).order_by(
            '-created_at')
        return context


# Vue pour la création d'un post
class PostCreateView(CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content']

    # Redirige dynamiquement vers le détail du post créé
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    # S'assure que l'auteur du post est bien l'utilisateur connecté
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Vue pour la modification d'un post
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content']

    # Redirige dynamiquement vers le détail du post modifié
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    # S'assure que l'utilisateur ne peut modifier que ses propres posts
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


# Vue pour la suppression d'un post
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'

    # Redirige dynamiquement vers le détail du post créé
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    # S'assure que l'utilisateur ne peut supprimer que ses propres posts
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


# Vue pour l'affichage du détail d'une review dans le contexte de son post
class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review_detail.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.object

        # Récupérer le post concerné par la critique
        context['post'] = review.post

        # Récupérer toutes les critiques du post
        context['reviews'] = review.post.reviews.all()

        return context


# Vue pour la création d'une review
class ReviewCreateView(CreateView):
    model = Review
    template_name = 'review_form.html'
    fields = ['post', 'title', 'content']

    # Redirige vers le détail du post contenant la review créée
    def get_success_url(self):
        return reverse_lazy('review_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Vue pour la modification d'une review
class ReviewUpdateView(UpdateView):
    model = Review
    template_name = 'review_form.html'
    fields = ['post', 'title', 'content']

    # Redirige vers le détail du post contenant la review créée
    def get_success_url(self):
        return reverse_lazy('review_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)


# Vue pour la suppression d'une review
class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'

    # Redirige vers le détail du post contenant la review créée
    def get_success_url(self):
        return reverse_lazy('review_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)
