# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Meta:
        db_table = 'auth_user'
