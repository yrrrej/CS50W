from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'

class Post(models.Model):

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    content=models.CharField(max_length=255, blank=True)

    def serailize(self):
        return {
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "id":self.id,
            "likes": self.likes.count(),
        }

class Like(models.Model):
    post=models.ManyToManyField('Post', related_name="likes")
    user=models.ForeignKey("User", on_delete=models.CASCADE, related_name="likedon")

class Follow(models.Model):
    user=models.ForeignKey("User", on_delete=models.CASCADE,related_name='userfollowing')
    following=models.ManyToManyField("User", related_name="following",null=True,blank=True)

class Followers(models.Model):
    user=models.ForeignKey("User", on_delete=models.CASCADE,related_name='userfollower')
    follower=models.ManyToManyField("User", related_name="follower",null=True,blank=True)