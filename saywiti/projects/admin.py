# -*- coding: utf-8 -*-
from django.contrib.gis import admin

from .models import Project, Category, Issue


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active', 'project')


@admin.register(Issue)
class IssueAdmin(admin.OSMGeoAdmin):

    list_display = ('title', 'category', 'point')
    search_fields = ('title',)
    list_filter = ('category', 'project')
