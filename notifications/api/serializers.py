#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.humanize.templatetags.humanize import naturaltime

from rest_framework import serializers

from notifications.models import Notification
from users.api.serializers import UserDetailSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a report.
    """
    Actor = UserDetailSerializer(read_only=True)
    notification_string = serializers.SerializerMethodField()
    created_naturaltime = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_string',
            'Actor',
            'Object',
            'is_read',
            'created',
            'created_naturaltime',
        ]

    def get_notification_string(self, obj):
        """Returns string representation of notification."""
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
