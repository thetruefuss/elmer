#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.humanize.templatetags.humanize import naturaltime

from rest_framework import serializers

from boards.models import Board
from users.api.serializers import UserDetailSerializer


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a board.
    """
    admins = UserDetailSerializer(read_only=True, many=True)
    subscribers_count = serializers.SerializerMethodField()
    created = serializers.DateTimeField(read_only=True)
    created_naturaltime = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    total_posts = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'cover',
            'cover_url',
            'total_posts',
            'admins',
            'subscribers_count',
            'created',
            'created_naturaltime',
            'is_subscribed',
            'is_admin',
        ]

    def get_admins(self, obj):
        """Returns a list of admins."""
        return obj.get_admins()

    def get_total_posts(self, obj):
        """Calculates number of total posts in a board."""
        return obj.submitted_subjects.count()

    def get_cover_url(self, obj):
        """Returns board cover url."""
        request = self.context.get('request')
        cover_url = obj.get_picture()
        return request.build_absolute_uri(cover_url)

    def get_subscribers_count(self, obj):
        """Calculates number of subscribers."""
        return obj.subscribers.all().count()

    def get_is_subscribed(self, obj):
        """Checks if user is subscribed to the board."""
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.subscribers.all():
            return True
        return False

    def get_created_naturaltime(self, obj):
        """Returns human readable time."""
        return naturaltime(obj.created)

    def get_is_admin(self, obj):
        """Checks if user is admin."""
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.admins.all():
            return True
        return False

    def create(self, validated_data):
        """Handles the creation of board."""
        instance = self.Meta.model(**validated_data)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        instance.save()
        instance.admins.add(user)
        instance.subscribers.add(user)
        instance.save()
        return instance
