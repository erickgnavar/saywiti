from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^projects/(?P<slug>[\w-]+)/$', views.ProjectDetailView.as_view(), name='project-detail'),
    url(r'^issues/(?P<id>\d+)/$', views.IssueDetailView.as_view(), name='issue-detail'),
]
