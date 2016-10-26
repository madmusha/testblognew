# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


class Blog(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return "%s, %s"%(self.author.username, self.slug)


def blog_post_save_reciever(sender, instance, created, *args, **kwargs):
    if created:
        slug = slugify(instance.author.username)
        instance.slug = slug
        instance.save()

post_save.connect(blog_post_save_reciever, sender=Blog)


class Post(models.Model):
    author = models.ForeignKey(User)
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=256)
    body = models.TextField(max_length=16000)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ["-timestamp"]

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"blog_slug":self.blog.slug, "post_pk":self.id})


    def __str__(self):
        return "%s, %s"%(self.author.username, self.title)

def newpost_post_save_reciever(sender, instance, created, *args, **kwargs):
    if created:
        qs = User.objects.filter(userprofile__subs__in=[instance.blog])
        recipients = [x[0] for x in qs.values_list('email')]

        subject = u'Новый пост в вашей ленте'
        text_content = u'Новый пост вы можете прочитать по ссылке %s' % (instance.get_absolute_url())
        sender = settings.EMAIL_HOST_USER

        send_mail(subject, text_content, sender, recipients, fail_silently=True)


post_save.connect(newpost_post_save_reciever, sender=Post)