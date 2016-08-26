# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis import admin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Post)
class PostAdmin(admin.OSMGeoAdmin):

    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)
    modifiable = False
