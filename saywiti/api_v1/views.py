# -*- coding: utf-8 -*-
import json
from django.http import JsonResponse
from django.core.urlresolvers import reverse

from saywiti.posts.models import Post
from saywiti.projects.models import Issue


def posts(request):
    posts = Post.objects.all()
    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'name': post.name,
            'icon': post.marker_icon,
            'latitude': post.latitude,
            'longitude': post.longitude,
            'point': json.loads(post.point.geojson),
            'url': reverse('api_v1:post-detail', kwargs={'post_id': post.id}),
            'category_id': post.category_id
        })
    return JsonResponse({'data': data})


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        data = {
            'name': post.name,
            'content': post.html_content
        }
        return JsonResponse({'data': data})
    except Post.DoesNotExists:
        return JsonResponse({
            'message': 'not found'
        }, status=404)


def issue_list(request, slug):
    # TODO: find a better way to add host
    host = "{}://{}".format(request.scheme, request.get_host())
    issues = Issue.objects.filter(project__slug=slug)
    rendered_issues = list(map(lambda x: render_issue(x, host), issues))
    return JsonResponse({'data': rendered_issues})


def render_issue(issue, host):
    return {
        'id': issue.id,
        'title': issue.title,
        'content': issue.content,
        'point': json.loads(issue.point.geojson),
        'category_icon': host + issue.marker_icon,
        'detail_url': host + reverse('projects:issue-detail', kwargs={'id': issue.id})
    }
