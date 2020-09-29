from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

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

class Follow(models.Model):

    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follows")
    followed = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.follower} - {self.followed} | {self.timestamp}"

    class Meta:
        unique_together = ("follower", "followed")

class Like(models.Model):

    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f" {self.user} - {self.post}"

    class Meta:
        unique_together = ("user", "post")
