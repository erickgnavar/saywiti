# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(TimeStampedModel, self).save(*args, **kwargs)
