#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime

from rest_framework import serializers

from comments.models import Comment
from notifications.models import Notification
from users.api.serializers import UserDetailSerializer


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a comment.
    """
    commenter = UserDetailSerializer(read_only=True)
    is_commenter = serializers.SerializerMethodField()
    created_naturaltime = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'body',
            'subject',
            'commenter',
            'is_commenter',
            'created',
            'created_naturaltime',
        ]

    def get_is_commenter(self, obj):
        """Checks if user is the commenter."""
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user == obj.commenter:
            return True
        return False

    def get_created_naturaltime(self, obj):
        """Returns human readable time."""
        return naturaltime(obj.created)

    def create(self, validated_data):
        """Handles the creation of comment."""
        instance = self.Meta.model(**validated_data)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        instance.save()

        # Use celery to create notifications in the background.
        subject = validated_data['subject']
        if user is not subject.author:
            Notification.objects.create(Actor=user, Object=subject, Target=subject.author, notif_type='comment')
        # Checks if someone is mentioned in the comment
        body = validated_data['body']
        words_list = body.split(" ")
        names_list = []
        for word in words_list:
            # if first two letters of the word is "u/" then the rest of the word
            # will be treated as a username
            if word[:2] == "u/":
                username = word[2:]
                try:
                    mentioned_user = User.objects.get(username=username)
                    if mentioned_user not in names_list:
                        if user is not mentioned_user:
                            Notification.objects.create(Actor=user,
                                                        Object=subject,
                                                        Target=mentioned_user,
                                                        notif_type='comment_mentioned')
                        names_list.append(mentioned_user)
                except:  # noqa: E722
                    pass
        return instance
