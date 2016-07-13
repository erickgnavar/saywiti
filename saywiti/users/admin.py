# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):

    list_display = ('username', 'email', 'is_superuser')
    search_fields = ('username', 'email')
