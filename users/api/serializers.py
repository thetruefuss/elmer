#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class CurrentUserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a current user details.
    """

    screen_name = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'screen_name',
            'profile_picture',
        ]

    def get_screen_name(self, obj):
        """
        Returns user screen name.

        :return: string
        """
        return obj.profile.screen_name()

    def get_profile_picture(self, obj):
        """
        Returns user's profile picture link.

        :return: string
        """
        request = self.context.get('request')
        profile_picture_url = obj.profile.get_picture()
        return request.build_absolute_uri(profile_picture_url)


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a user details.
    """

    screen_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['screen_name', 'username']

    def get_screen_name(self, obj):
        """
        Returns user screen name.

        :return: string
        """
        return obj.profile.screen_name()


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a user login process.
    """

    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password', 'token']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        """
        Validates user data & returns token in case provided credentials are correct.

        :params data: dict
        :return: dict
        """
        username = data['username']
        password = data['password']
        user_qs = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).distinct()
        if user_qs.exists() and user_qs.count() == 1:
            user_obj = user_qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                data['token'] = token
            else:
                raise serializers.ValidationError("Incorrect password.")
        else:
            raise serializers.ValidationError("The user with this username does not exists.")
        return data


class UserSerializerWithToken(serializers.ModelSerializer):
    """
    Serializer that represents a user registration.
    """

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        """
        Generates JWT.

        :return: string
        """
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        """
        Handles the creation of user.

        :params validated_data: dict
        :return: string
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = [
            'token',
            'username',
            'email',
            'password',
        ]


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a profile.
    """
    profile_picture_url = serializers.SerializerMethodField()
    screen_name = serializers.SerializerMethodField()
    requester_in_contact_list = serializers.SerializerMethodField()
    requester_in_pending_list = serializers.SerializerMethodField()
    has_followed = serializers.SerializerMethodField()
    is_requesters_profile = serializers.SerializerMethodField()
    created_boards_count = serializers.SerializerMethodField()
    posted_subjects_count = serializers.SerializerMethodField()
    boards_subsribed_count = serializers.SerializerMethodField()
    member_since = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'profile_picture_url',
            'screen_name',
            'requester_in_contact_list',
            'requester_in_pending_list',
            'has_followed',
            'is_requesters_profile',
            'created_boards_count',
            'posted_subjects_count',
            'boards_subsribed_count',
            'member_since',
        ]

    def get_profile_picture_url(self, obj):
        """
        Returns user's profile picture url.

        :return: string
        """
        request = self.context.get('request')
        profile_picture_url = obj.profile.get_picture()
        return request.build_absolute_uri(profile_picture_url)

    def get_screen_name(self, obj):
        """
        Returns user's screen name.

        :return: string
        """
        return obj.profile.screen_name()

    def get_requester_in_contact_list(self, obj):
        """
        Check if requester is in user's contact list.

        :return: boolean
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.profile.contact_list.all():
            return True
        return False

    def get_requester_in_pending_list(self, obj):
        """
        Check if requester is in user's pending list.

        :return: boolean
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.profile.pending_list.all():
            return True
        return False

    def get_is_requesters_profile(self, obj):
        """
        Check if requester is the user.

        :return: boolean
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user == obj:
            return True
        return False

    def get_has_followed(self, obj):
        """
        Check if requester has followed the user.

        :return: boolean
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.profile.followers.all():
            return True
        return False

    def get_created_boards_count(self, obj):
        """
        Counts user's created boards.

        :return: integer
        """
        return obj.inspected_boards.count()

    def get_posted_subjects_count(self, obj):
        """
        Counts user's posted subjects.

        :return: integer
        """
        return obj.posted_subjects.count()

    def get_boards_subsribed_count(self, obj):
        """
        Counts user's subscribed boards.

        :return: integer
        """
        return obj.subscribed_boards.count()

    def get_member_since(self, obj):
        """
        Returns date of user's profile creation.

        :return: string
        """
        return obj.profile.member_since.date()
