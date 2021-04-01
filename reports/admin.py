#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Report


class ReportAdmin(admin.ModelAdmin):
    """
    Admin settings for reports.
    """
    list_display = ('reporter', 'created', 'active')
    list_filter = ('active', )
    date_hierarchy = 'created'


admin.site.register(Report, ReportAdmin)  # noqa: E305
