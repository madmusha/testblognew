# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from blog.models import Blog, Post
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    read = models.ManyToManyField(Post, blank=True)
    subs = models.ManyToManyField(Blog, blank=True)

    def __str__(self):
        return self.user.username


from django.db.models.signals import post_save

def user_post_save_reciever(sender, instance, created, *args, **kwargs):
    if created:
        profile = UserProfile.objects.get_or_create(user=instance)[0]
        blog = Blog.objects.get_or_create(author=instance)[0]


post_save.connect(user_post_save_reciever, sender=User)