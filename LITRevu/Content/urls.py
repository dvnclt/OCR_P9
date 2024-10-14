from django.urls import path

from .views import PostListView, ReviewListView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
]
