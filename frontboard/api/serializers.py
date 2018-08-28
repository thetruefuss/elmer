from django.contrib.humanize.templatetags.humanize import naturaltime

from frontboard.models import Board, Comment, Subject
from rest_framework import serializers
from user_accounts.api.serializers import UserDetailSerializer


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
            'id', 'title', 'slug', 'body', 'body_linkified',
            'photo', 'author', 'board', 'board_slug', 'stars_count',
            'comments_count', 'is_starred', 'created',
            'created_naturaltime', 'is_author',
        ]

    def get_body_linkified(self, obj):
        """
        Linkifies the body.

        :return: string
        """
        return obj.linkfy_subject()

    def get_board_slug(self, obj):
        """
        Returns board slug.

        :return: string
        """
        return obj.board.slug

    def get_stars_count(self, obj):
        """
        Counts stars on subject.

        :return: integer
        """
        return obj.points.all().count()

    def get_comments_count(self, obj):
        """
        Counts comments on subject.

        :return: integer
        """
        return obj.comments.all().count()

    def get_is_starred(self, obj):
        """
        Check if user has starred subject.

        :return: boolean
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.points.all():
            return True
        return False

    def get_created_naturaltime(self, obj):
        """
        Returns human readable time.

        :return: string
        """
        return naturaltime(obj.created)

    def get_is_author(self, obj):
        """
        Checks if user is the author of the subject.

        :return: boolean
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user == obj.author:
            return True
        return False


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
            'id', 'title', 'slug', 'description', 'cover', 'cover_url',
            'total_posts', 'admins', 'subscribers_count', 'created',
            'created_naturaltime', 'is_subscribed', 'is_admin',
        ]

    def get_admins(self, obj):
        """
        Returns a list of admins.

        :return: list.
        """
        return obj.get_admins()

    def get_total_posts(self, obj):
        """
        Calculates number of total posts in a board.

        :return: integer
        """
        return obj.submitted_subjects.count()

    def get_cover_url(self, obj):
        """
        Returns board cover url.

        :return: string
        """
        request = self.context.get('request')
        cover_url = obj.get_picture()
        return request.build_absolute_uri(cover_url)

    def get_subscribers_count(self, obj):
        """
        Calculates number of subscribers.

        :return: integer
        """
        return obj.subscribers.all().count()

    def get_is_subscribed(self, obj):
        """
        Checks if user is subscribed to the board.

        :return: boolean
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.subscribers.all():
            return True
        return False

    def get_created_naturaltime(self, obj):
        """
        Returns human readable time.

        :return: string
        """
        return naturaltime(obj.created)

    def get_is_admin(self, obj):
        """
        Checks if user is admin.

        :return: boolean
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.admins.all():
            return True
        return False

    def create(self, validated_data):
        """
        Handles the creation of board.

        :params validated_data: dict
        :return: string
        """
        instance = self.Meta.model(**validated_data)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        instance.save()
        instance.admins.add(user)
        instance.subscribers.add(user)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    commenter = UserDetailSerializer(read_only=True)
    is_commenter = serializers.SerializerMethodField()
    created_naturaltime = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'body', 'subject', 'commenter', 'is_commenter', 'created', 'created_naturaltime',
        ]

    def get_is_commenter(self, obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user == obj.commenter:
            return True
        return False

    def get_created_naturaltime(self, obj):
        return naturaltime(obj.created)
