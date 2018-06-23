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
    url = serializers.HyperlinkedIdentityField(
        view_name='frontboard-api:subjects_retrieve',
        lookup_field='slug'
    )
    author = UserDetailSerializer(read_only=True)
    board = serializers.SerializerMethodField()
    body_linkify = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'url', 'title', 'body', 'body_linkify',
            'photo', 'author', 'board', 'like_count',
            'comment_count'
        ]

    def get_board(self, obj):
        return str(obj.board.slug)

    def get_body_linkify(self, obj):
        return obj.linkfy_subject()

    def get_like_count(self, obj):
        return obj.points.all().count()

    def get_comment_count(self, obj):
        return obj.comments.all().count()


class SubjectRetrieveSerializer(serializers.ModelSerializer):
    comments_url = serializers.HyperlinkedIdentityField(
        view_name='frontboard-api:comments_list',
        lookup_field='slug'
    )
    points = serializers.SerializerMethodField()
    author = UserDetailSerializer(read_only=True)
    board = serializers.SerializerMethodField()
    body_linkify = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'id', 'title', 'slug', 'body', 'body_linkify',
            'photo', 'author', 'board', 'points',
            'like_count', 'comment_count', 'comments_url'
        ]

    def get_points(self, obj):
        return str(obj.points.all())

    def get_board(self, obj):
        return str(obj.board.slug)

    def get_body_linkify(self, obj):
        return obj.linkfy_subject()

    def get_like_count(self, obj):
        return obj.points.all().count()

    def get_comment_count(self, obj):
        return obj.comments.all().count()


class BoardCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            'title', 'description', 'cover',
        ]


class BoardListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='frontboard-api:boards_retrieve',
        lookup_field='slug'
    )

    class Meta:
        model = Board
        fields = [
            'url', 'title', 'description',
        ]


class BoardRetrieveSerializer(serializers.ModelSerializer):
    admins = serializers.SerializerMethodField()
    subscribers = serializers.SerializerMethodField()
    subscribers_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'slug', 'description', 'cover',
            'admins', 'subscribers', 'subscribers_count', 'created',
        ]

    def get_admins(self, obj):
        return str(obj.get_admins())

    def get_subscribers(self, obj):
        return str(obj.subscribers.all())

    def get_subscribers_count(self, obj):
        return str(obj.subscribers.all().count())


class CommentListSerializer(serializers.ModelSerializer):
    commenter = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'body', 'commenter', 'created'
        ]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'body', 'subject'
        ]
