#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin settings for profiles.
    """
    list_display = ('user', 'dob', 'member_since')
    date_hierarchy = 'member_since'


admin.site.register(Profile, ProfileAdmin)  # noqa: E305
