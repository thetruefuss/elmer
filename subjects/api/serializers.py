#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime

from rest_framework import serializers

from notifications.models import Notification
from subjects.models import Subject
from users.api.serializers import UserDetailSerializer


class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a subject.
    """
    body_linkified = serializers.SerializerMethodField()
    author = UserDetailSerializer(read_only=True)
    board_slug = serializers.SerializerMethodField()
    stars_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    created = serializers.DateTimeField(read_only=True)
    created_naturaltime = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'id',
            'title',
            'slug',
            'body',
            'body_linkified',
            'photo',
            'author',
            'board',
            'board_slug',
            'stars_count',
            'comments_count',
            'is_starred',
            'created',
            'created_naturaltime',
            'is_author',
        ]

    def get_body_linkified(self, obj):
        """Linkifies the body."""
        return obj.linkfy_subject()

    def get_board_slug(self, obj):
        """Returns board slug."""
        return obj.board.slug

    def get_stars_count(self, obj):
        """Counts stars on subject."""
        return obj.points.all().count()

    def get_comments_count(self, obj):
        """Counts comments on subject."""
        return obj.comments.all().count()

    def get_is_starred(self, obj):
        """Check if user has starred subject."""
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.points.all():
            return True
        return False

    def get_created_naturaltime(self, obj):
        """Returns human readable time."""
        return naturaltime(obj.created)

    def get_is_author(self, obj):
        """Checks if user is the author of the subject."""
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user == obj.author:
            return True
        return False

    def create(self, validated_data):
        """Handles the creation of board."""
        instance = self.Meta.model(**validated_data)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        instance.save()

        # Use celery to create notifications in the background.
        title = validated_data['title']
        body = validated_data['body']

        # Checks if someone is mentioned in the subject
        words = title + ' ' + body
        words_list = words.split(" ")
        names_list = []
        for word in words_list:

            # if first two letter of the word is "u/" then the rest of the word
            # will be treated as a username

            if word[:2] == "u/":
                username = word[2:]
                try:
                    mentioned_user = User.objects.get(username=username)
                    if mentioned_user not in names_list:
                        instance.mentioned.add(user)
                        if user is not mentioned_user:
                            Notification.objects.create(Actor=user,
                                                        Object=instance,
                                                        Target=mentioned_user,
                                                        notif_type='subject_mentioned')
                        names_list.append(user)
                except:  # noqa: E722
                    pass
        return instance
