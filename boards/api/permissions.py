#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    message = "You are not the admin of this board."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user in obj.admins.all():
            return True
