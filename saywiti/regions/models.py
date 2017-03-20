# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.postgres.fields.jsonb import JSONField
from django.utils.translation import ugettext_lazy as _

from saywiti.common.models import TimeStampedModel


class Level(TimeStampedModel):

    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)

    name = models.CharField(_('Name'), max_length=100)
    description = models.CharField(_('Description'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Region(TimeStampedModel):

    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    level = models.ForeignKey('Level', related_name='regions')

    name = models.CharField(_('Name'), max_length=100)
    is_osm_relation = models.BooleanField(_('Is an OSM relation?'), default=False)
    osm_tags = JSONField(_('OSM Tags'), null=True, blank=True)
    osm_relation_id = models.IntegerField(_('OSM Relation ID'), null=True, blank=True)

    polygon = models.PolygonField()

    def __str__(self):
        return self.name
