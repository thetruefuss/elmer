from django.contrib.humanize.templatetags.humanize import naturaltime

from frontboard.models import Board, Comment, Subject
from rest_framework import serializers
from user_accounts.api.serializers import UserDetailSerializer


class SubjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'title', 'body', 'photo', 'board',
        ]


class SubjectListSerializer(serializers.ModelSerializer):
    body_linkified = serializers.SerializerMethodField()
    author = UserDetailSerializer(read_only=True)
    board = serializers.SerializerMethodField()
    stars_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    created_naturaltime = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'id', 'title', 'slug', 'body', 'body_linkified',
            'photo', 'author', 'board', 'stars_count',
            'comments_count', 'is_starred', 'created',
            'created_naturaltime',
        ]

    def get_body_linkified(self, obj):
        return obj.linkfy_subject()

    def get_board(self, obj):
        return str(obj.board.slug)

    def get_stars_count(self, obj):
        return obj.points.all().count()

    def get_comments_count(self, obj):
        return obj.comments.all().count()

    def get_is_starred(self, obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.points.all():
            return True
        return False

    def get_created_naturaltime(self, obj):
        return naturaltime(obj.created)


class SubjectRetrieveSerializer(serializers.ModelSerializer):
    body_linkified = serializers.SerializerMethodField()
    author = UserDetailSerializer(read_only=True)
    board = serializers.SerializerMethodField()
    stars_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    created_naturaltime = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'id', 'title', 'slug', 'body', 'body_linkified',
            'photo', 'author', 'board', 'stars_count',
            'comments_count', 'is_starred', 'created',
            'created_naturaltime', 'is_author',
        ]

    def get_body_linkified(self, obj):
        return obj.linkfy_subject()

    def get_board(self, obj):
        return str(obj.board.slug)

    def get_stars_count(self, obj):
        return obj.points.all().count()

    def get_comments_count(self, obj):
        return obj.comments.all().count()

    def get_is_starred(self, obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.points.all():
            return True
        return False

    def get_created_naturaltime(self, obj):
        return naturaltime(obj.created)

    def get_is_author(self, obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user == obj.author:
            return True
        return False


class BoardCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            'title', 'slug', 'description', 'cover',
        ]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        instance.save()
        instance.admins.add(user)
        instance.subscribers.add(user)
        instance.save()
        return instance


class BoardListSerializer(serializers.ModelSerializer):
    subscribers_count = serializers.SerializerMethodField()
    created_naturaltime = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'slug', 'description', 'subscribers_count',
            'created', 'created_naturaltime', 'is_subscribed',
        ]

    def get_subscribers_count(self, obj):
        return str(obj.subscribers.all().count())

    def get_is_subscribed(self, obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.subscribers.all():
            return True
        return False

    def get_created_naturaltime(self, obj):
        return naturaltime(obj.created)


class BoardRetrieveSerializer(serializers.ModelSerializer):
    admins =  UserDetailSerializer(read_only=True, many=True)
    subscribers = UserDetailSerializer(read_only=True, many=True)
    subscribers_count = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    total_posts = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'slug', 'description', 'cover', 'total_posts',
            'admins', 'subscribers', 'subscribers_count', 'created',
        ]

    def get_total_posts(self, obj):
        return str(obj.submitted_subjects.count())

    def get_cover(self, obj):
        request = self.context.get('request')
        cover_url = obj.get_picture()
        return request.build_absolute_uri(cover_url)

    def get_admins(self, obj):
        return str(obj.get_admins())

    def get_subscribers(self, obj):
        return str(obj.subscribers.all())

    def get_subscribers_count(self, obj):
        return str(obj.subscribers.all().count())


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
