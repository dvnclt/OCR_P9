from django.urls import path

from .views import (
    PostCreateView, PostUpdateView, PostDeleteView,
    ReviewCreateView, ReviewUpdateView, ReviewDeleteView,
    PostReviewCreateView, FeedView
    )

urlpatterns = [
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(),
         name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(),
         name='post_delete'),


    path('reviews/new/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(),
         name='review_update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(),
         name='review_delete'),

    path('post-review/new/', PostReviewCreateView.as_view(),
         name='post-review_create'),
    path('feed/', FeedView.as_view(), name='feed')
]
