# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import get_thumbnail

from saywiti.common.models import TimeStampedModel


class Category(TimeStampedModel):

    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(max_length=255, editable=False)
    is_active = models.BooleanField(_('Is active?'), default=True)
    icon = models.ImageField(_('Icon'), upload_to='category/icons/%Y/%m/%d/')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @property
    def marker_icon(self):
        im = get_thumbnail(self.icon, '40x40')
        return im.url


class Post(TimeStampedModel):

    category = models.ForeignKey('Category', related_name='posts')
    region = models.ForeignKey('regions.Region', related_name='posts', null=True, blank=True)

    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(max_length=255, editable=False)

    markdown_content = models.TextField(_('Content'), blank=True)
    html_content = models.TextField(editable=False, null=True)

    latitude = models.FloatField(_('Latitude'), null=True, blank=True)
    longitude = models.FloatField(_('Longitude'), null=True, blank=True)

    point = models.PointField(null=True, blank=True,
                              help_text=_('This field will be updated with the content of latitude and longitude fields'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self._create_point()
        self._compile()
        return super().save(*args, **kwargs)

    def _create_point(self):
        if self.latitude and self.longitude:
            self.point = Point(self.longitude, self.latitude)
        else:
            self.point = None

    def _compile(self):
        """
        Compile markdown to html content
        """
        self.html_content = self.markdown_content
        # TODO: implement this

    @property
    def marker_icon(self):
        im = get_thumbnail(self.category.icon, '40x40')
        return im.url
