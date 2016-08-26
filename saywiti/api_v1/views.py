# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.http import JsonResponse

from saywiti.posts.models import Post


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
