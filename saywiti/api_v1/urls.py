# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^posts/(?P<post_id>\d+)/$', views.post_detail, name='post-detail'),
    url(r'^projects/(?P<slug>[\w-]+)/issues/$', views.issue_list, name='issue-list'),
]
