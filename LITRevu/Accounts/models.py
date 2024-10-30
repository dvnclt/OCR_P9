from django.db import models
from django.contrib.auth.models import AbstractUser


class Member(AbstractUser):

    def __str__(self):
        return (f"{self.username} - {self.email}\n"
                f"{self.first_name} - {self.last_name}")


class Subscription(models.Model):
    following = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='followers'
    )
    follower = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='following'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} suit {self.following}"
