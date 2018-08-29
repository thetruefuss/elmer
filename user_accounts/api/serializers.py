from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from user_accounts.models import Profile, Notification

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


User = get_user_model()

class CurrentUserDetailSerializer(serializers.ModelSerializer):
    screen_name = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username', 'screen_name', 'profile_picture',
        ]

    def get_screen_name(self, obj):
        return str(obj.profile.screen_name())

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        profile_picture_url = obj.profile.get_picture()
        return request.build_absolute_uri(profile_picture_url)


class UserDetailSerializer(serializers.ModelSerializer):
    screen_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'screen_name', 'username'
        ]

    def get_screen_name(self, obj):
        return str(obj.profile.screen_name())


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'username', 'password', 'token'

        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        username = data['username']
        password = data['password']
        user_qs = User.objects.filter(
            Q(username__iexact=username)|
            Q(email__iexact=username)
        ).distinct()
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

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'email', 'password')


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('dp',)


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a report.
    """

    Actor = UserDetailSerializer(read_only=True)
    notification_string = serializers.SerializerMethodField()
    created_naturaltime = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'notification_string', 'Actor', 'Object', 'is_read',
            'created', 'created_naturaltime',
        ]

    def get_notification_string(self, obj):
        """
        Returns string representation of notification.

        :return: string
        """
        return str(obj)

    def get_is_commenter(self, obj):
        """
        Checks if user is the commenter.

        :return: boolean
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user == obj.commenter:
            return True
        return False

    def get_created_naturaltime(self, obj):
        """
        Returns human readable time.

        :return: string
        """
        return naturaltime(obj.created)
