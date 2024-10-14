from django.views.generic import ListView

from .models import Post, Review


class PostListView(ListView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


class ReviewListView(ListView):
    model = Review
    template_name = 'review.html'
    context_object_name = 'reviews'
    ordering = ['-created_at']
