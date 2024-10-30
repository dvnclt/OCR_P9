from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from Accounts.models import Member


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Review(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='reviews'
        )
    title = models.CharField(max_length=255)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f'Review by {self.author} on {self.post}'
