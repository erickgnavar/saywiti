# -*- coding: utf-8 -*-
from django.shortcuts import render

from saywiti.posts.models import Category


def home(request):
    categories = Category.objects.all()
    return render(request, 'web/map.html', {
        'categories': categories
    })
