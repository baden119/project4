from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    # This function is based off a similar one proveided with project 3
    # It is necessary if using JS to fetch posts for display
    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "user": self.user.username,
    #         "body": self.body,
    #         "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
    #         "likes": self.likes
    #     }
