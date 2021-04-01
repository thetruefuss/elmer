#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied

from .models import Board


def user_is_board_admin(f):
    def wrap(request, *args, **kwargs):
        board = Board.objects.get(slug=kwargs['board'])
        if request.user in board.admins.all():
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def user_is_not_banned_from_board(f):
    def wrap(request, *args, **kwargs):
        board = Board.objects.get(slug=kwargs['board'])
        if not request.user in board.banned_users.all():
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
