#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    """
    Admin settings for messages.
    """
    list_display = (
        'user',
        'conversation',
        'message',
        'date',
    )
    list_filter = ('date', )


admin.site.register(Message, MessageAdmin)  # noqa: E305
