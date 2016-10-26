# coding=utf-8
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import UserProfile
from blog.models import Blog, Post

# Create your views here.

def readed(request):
    if request.is_ajax():
        post = get_object_or_404(Post, pk = request.GET.get('pk'))
        if request.GET.get('tag')=='true':
            try:
                prof = UserProfile.objects.get(user=request.user)
                prof.read.add(post)
                return JsonResponse({'read': "success"})
            except:
                return JsonResponse({'read': "failure"})
        elif request.GET.get('tag') == 'false':
            try:
                prof = UserProfile.objects.get(user=request.user)
                prof.read.remove(post)
                return JsonResponse({'read': "success"})
            except:
                return JsonResponse({'read': "failure"})
    else:
        return Http404

def subscribe(request):
    if request.is_ajax():
        blog = get_object_or_404(Blog, pk = request.GET.get('pk'))
        if request.GET.get('tag')=='subscribe':
            try:
                prof = UserProfile.objects.get(user=request.user)
                prof.subs.add(blog)
                return JsonResponse({'read': "success", 'label': u"Отписаться", 'tag': 'unsubscribe'})
            except:
                return JsonResponse({'read': "failure"})
        elif request.GET.get('tag') == 'unsubscribe':
            try:
                prof = UserProfile.objects.get(user=request.user)
                prof.subs.remove(blog)
                for obj in blog.post_set.all():
                    prof.read.remove(obj)
                return JsonResponse({'read': "success", 'label': u"Подписаться", 'tag': 'subscribe'})
            except:
                return JsonResponse({'read': "failure"})
    else:
        return Http404