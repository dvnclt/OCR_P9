from django.db import models

from Accounts.models import Member


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Review(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='reviews'
        )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f'Review by {self.author} on {self.post}'
