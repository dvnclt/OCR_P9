from django.contrib.auth.models import AbstractUser


class Member(AbstractUser):

    def __str__(self):
        return (f"{self.username} - {self.email}\n"
                f"{self.first_name} - {self.last_name}")
