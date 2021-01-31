from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Comment(models.Model):
   text = models.TextField(max_length=254)
   datetime = models.DateTimeField(blank=False,null=False,auto_now=True) 
   user = models.ForeignKey('auth.User',related_name='comment_owner',on_delete=models.CASCADE)
   video = models.ForeignKey('Video',related_name='comment_owner',on_delete=models.CASCADE)
   def __str__(self):
         return 'comment'+'-'+str(self.user.id)
 
class Video(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=254)
    path = models.CharField(max_length=60)
    datetime = models.DateTimeField(blank=False,null=False,auto_now=True)
    user = models.ForeignKey('auth.User',related_name='video_owner',on_delete=models.CASCADE)
    def __str__(self):
         return self.title   
