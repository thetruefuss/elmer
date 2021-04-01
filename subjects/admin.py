#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Subject


class SubjectAdmin(admin.ModelAdmin):
    """
    Admin settings for subjects.
    """
    list_display = ('title', 'board', 'created', 'active')
    list_filter = ('title', 'active')
    date_hierarchy = 'created'


admin.site.register(Subject, SubjectAdmin)  # noqa: E305
