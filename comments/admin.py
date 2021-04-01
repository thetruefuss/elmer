#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    """
    Admin settings for comments.
    """
    list_display = ('body', 'commenter', 'created', 'active')
    list_filter = ('commenter', 'active')
    date_hierarchy = 'created'


admin.site.register(Comment, CommentAdmin)  # noqa: E305
