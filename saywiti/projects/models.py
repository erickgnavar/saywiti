# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import get_thumbnail

from saywiti.common.models import TimeStampedModel


class Project(TimeStampedModel):

    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(max_length=255, editable=False)
    is_active = models.BooleanField(_('Is active?'), default=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Category(TimeStampedModel):

    project = models.ForeignKey('Project')

    name = models.CharField(_('Name'), max_length=100)
    is_active = models.BooleanField(_('Is active?'), default=True)
    icon = models.ImageField(_('Icon'), upload_to='category/icons/%Y/%m/%d/')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        default_related_name = 'categories'

    def __str__(self):
        return self.name

    @property
    def marker_icon(self):
        im = get_thumbnail(self.icon, '40x40')
        return im.url


class Issue(TimeStampedModel):

    project = models.ForeignKey('Project')
    category = models.ForeignKey('Category')

    title = models.CharField(_('Title'), max_length=100)
    content = models.TextField(_('Content'))

    point = models.PointField(_('Point'))

    class Meta:
        verbose_name = _('Issue')
        verbose_name_plural = _('Issues')
        default_related_name = 'issues'

    def __str__(self):
        return self.title

    @property
    def marker_icon(self):
        im = get_thumbnail(self.category.icon, '40x40')
        return im.url
