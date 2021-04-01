#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.humanize.templatetags.humanize import naturaltime

from rest_framework import serializers

from reports.models import Report
from users.api.serializers import UserDetailSerializer


class ReportSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a report.
    """
    reporter = UserDetailSerializer(read_only=True)
    report_string = serializers.SerializerMethodField()
    created_naturaltime = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'report_string',
            'reporter',
            'comment',
            'subject',
            'board',
            'created',
            'created_naturaltime',
        ]

    def get_report_string(self, obj):
        """Returns string representation of report."""
        return str(obj)

    def get_is_commenter(self, obj):
        """Checks if user is the commenter."""
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user == obj.commenter:
            return True
        return False

    def get_created_naturaltime(self, obj):
        """Returns human readable time."""
        return naturaltime(obj.created)
