#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from subjects.models import Subject


class Notification(models.Model):
    """
    Model that represents a notification.
    """
    NOTIF_CHOICES = (
        ('subject_mentioned', 'Mentioned in Subject'),
        ('comment_mentioned', 'Mentioned in Comment'),
        ('comment', 'Comment on Subject'),
        ('follow', 'Followed by someone'),
        ('sent_msg_request', 'Sent a Message Request'),
        ('confirmed_msg_request', 'Sent a Message Request'),
    )

    Actor = models.ForeignKey(User, related_name='c_acts', on_delete=models.CASCADE)
    Object = models.ForeignKey(Subject, related_name='act_notif', null=True, blank=True, on_delete=models.SET_NULL)
    Target = models.ForeignKey(User, related_name='c_notif', on_delete=models.CASCADE)
    notif_type = models.CharField(max_length=500, choices=NOTIF_CHOICES, default='Comment on Subject')
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        """
        Unicode representation for a notification based on notification type.
        """
        if self.notif_type == 'comment':
            return '{} commented on your subject \"{}\".'.format(self.Actor.profile.screen_name(), self.Object)
        elif self.notif_type == 'subject_mentioned':
            return '{} mentioned you in his subject \"{}\".'.format(self.Actor.profile.screen_name(), self.Object)
        elif self.notif_type == 'follow':
            return '{} followed you.'.format(self.Actor.profile.screen_name())
        elif self.notif_type == 'sent_msg_request':
            return '{} sent you a message request.'.format(self.Actor.profile.screen_name())
        elif self.notif_type == 'confirmed_msg_request':
            return '{} accepted your message request.'.format(self.Actor.profile.screen_name())
        else:
            return '{} mentioned you in his comment on subject \"{}\".'.format(self.Actor.profile.screen_name(),
                                                                               self.Object)

    @staticmethod
    def get_user_notification(user):
        """Returns user notifications."""
        if user:
            notifications = Notification.objects.filter(Target=user).exclude(Actor=user)
            return notifications
        return []
