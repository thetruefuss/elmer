#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied

from .models import Comment


def user_is_comment_owner(f):
    def wrap(request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs['pk'])
        if request.user == comment.commenter:
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
