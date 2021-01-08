from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    likes = models.ManyToManyField("Post", blank=True, related_name="liked_post")
    followers = models.ManyToManyField("self", blank="True", symmetrical=False, related_name="following")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_user")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialise(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "text": self.text,
            "likes": [user.likes for user in self.likes.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %#I:%M %p")
        }