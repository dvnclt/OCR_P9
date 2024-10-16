from django.urls import path

from .views import (
    PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView
    )

urlpatterns = [
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(),
         name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(),
         name='post_delete'),


    path('reviews/<int:pk>/', ReviewDetailView.as_view(),
         name='review_detail'),
    path('reviews/new/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(),
         name='review_update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(),
         name='review_delete'),
]
