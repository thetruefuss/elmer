#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from notifications.models import Notification

from .serializers import NotificationSerializer


class NotificationListAPIView(ListAPIView):
    """
    View that returns notification list of a single user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Notification.get_user_notification(self.request.user)
        unread_notifications = queryset_list.filter(is_read=False)
        # Add celery or something to alter the is_read flag in background
        # So this flag could be used in front end for styling purposes
        for notification in unread_notifications:
            notification.is_read = True
            notification.save()
        return queryset_list
