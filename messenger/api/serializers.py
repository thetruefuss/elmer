from django.contrib.auth.models import User

from messenger.models import Message
from rest_framework import serializers
from user_accounts.api.serializers import UserDetailSerializer


class ContactsListSerializer(serializers.ModelSerializer):
    screen_name = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    url_to = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'screen_name', 'profile_picture', 'url_to',
        ]

    def get_screen_name(self, obj):
        return obj.profile.screen_name()

    def get_profile_picture(self, obj):
        return obj.profile.get_picture()

    def get_url_to(self, obj):
        return "/api/messages/chat/?username={}".format(obj.username)


class MessageListSerializer(serializers.ModelSerializer):
    from_user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'from_user', 'message', 'date',
        ]
