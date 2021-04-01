#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from mysite.decorators import ajax_required

from .models import Notification


class ActivitiesPageView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the activities list per user."""
    model = Notification
    paginate_by = 20
    template_name = 'notifications/activities.html'
    context_object_name = 'events'

    def get_queryset(self, **kwargs):
        subject_events = Notification.objects.filter(Target=self.request.user).exclude(Actor=self.request.user)
        # Do this with celery.
        unread_subject_events = subject_events.filter(is_read=False)
        for notification in unread_subject_events:
            notification.is_read = True
            notification.save()
        return subject_events


@login_required
@ajax_required
def check_activities(request):
    subject_events = Notification.objects.filter(Target=request.user, is_read=False).exclude(Actor=request.user)
    return HttpResponse(len(subject_events))
