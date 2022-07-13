# from django.contrib.auth.models import User
import profile
from django.contrib.auth import get_user_model
from django.db import models
import uuid
User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user      = models.IntegerField()
    bio          = models.TextField(blank=True)
    profileimg   = models.ImageField(upload_to='profile_pics/', default='default-profile.png')
    location     = models.CharField(max_length=300, blank=True)
    birth_date   = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField( max_length=100)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return "Post id.{} ".format( self.id,)
class LikePost(models.Model):
    post_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    def __str__(self):
        return "Post id.{} by {} ".format( self.post_id, self.username)

class comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ('{}.{}').format(self.id, self.comment)