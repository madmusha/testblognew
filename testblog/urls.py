"""testblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from blog.views import PostDetailView, PostListView, Newsletter, PostCreateView
from userprofile.views import readed, subscribe
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', login, {'template_name':'login.html', 'redirect_authenticated_user': True}, name='login'),
    url(r'^logout/$', logout, {'next_page': 'login'}, name='logout'),
    url(r'^news/$', Newsletter.as_view(), name="news"),
    url(r'^admin/', admin.site.urls),
    url(r'^posts/$', PostListView.as_view(), name="posts_list"),
    url(r'^posts/create/$', PostCreateView.as_view(), name="posts_create"),
    url(r'^posts/readed/', readed, name="readed"),
    url(r'^blogs/subs/', subscribe, name="subs"),
    url(r'^(?P<blog_slug>[\w-]+)/(?P<post_pk>\d+)/', PostDetailView.as_view(), name="post_detail"),

]
