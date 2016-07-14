# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis import admin
from django.utils.html import format_html

from .models import Level, Region


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):

    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)


@admin.register(Region)
class RegionAdmin(admin.OSMGeoAdmin):

    list_display = ('name', 'level', 'parent', 'is_osm_relation', 'osm_relation_id', 'osm_link', 'osm_edit_link')
    search_fields = ('name',)
    list_filter = ('level', 'is_osm_relation', 'parent')

    def osm_link(self, obj):
        url = 'https://openstreetmap.org/relation/{}'.format(obj.osm_relation_id)
        link = '<a href="{}">{}</a>'
        return format_html(link, url, obj.osm_relation_id)

    def osm_edit_link(self, obj):
        url = 'https://openstreetmap.org/edit?editor=id&relation={}'.format(obj.osm_relation_id)
        link = '<a href="{}">{}</a>'
        return format_html(link, url, obj.osm_relation_id)
