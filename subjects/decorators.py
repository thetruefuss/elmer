#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied

from .models import Subject


def user_is_subject_author(f):
    def wrap(request, *args, **kwargs):
        subject = Subject.objects.get(slug=kwargs['subject'])
        if request.user == subject.author:
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
