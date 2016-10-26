from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site

from blog.signals import new_notification, notify
from .models import Blog, Post


class PostListView(ListView):
    model = Post

class PostDetailView(DetailView):
    model = Post

    def get_object(self):
        blog = get_object_or_404(Blog, slug=self.kwargs.get('blog_slug'))
        return get_object_or_404(Post, pk=self.kwargs.get('post_pk'))


class Newsletter(ListView):
    model = Post
    template_name = "blog/post_list.html"

    def get_queryset(self):
        qs = super(Newsletter, self).get_queryset()
        subs = self.request.user.userprofile.subs.all()
        return qs.filter(blog__in=subs)

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'body']

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.author = self.request.user
        blog = get_object_or_404(Blog, author=self.request.user)
        new_post.blog = blog
        new_post.save()
        notify.send(new_post, domain=get_current_site(self.request).domain)
        return HttpResponseRedirect(reverse("post_detail", kwargs={'blog_slug': blog.slug, 'post_pk': new_post.pk}))

