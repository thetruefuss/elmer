#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCommenterOrReadOnly(BasePermission):
    message = "Only commenter can delete the comment."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.commenter == request.user
