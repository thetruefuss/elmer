from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from user_accounts.models import Profile

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



class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password'
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        # do validation here
        return data

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get('email')
        user_obj = User.objects.get(email=email)
        if user_obj.exists():
            raise ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        profile = Profile.objects.create(user=user_obj)
        return validated_data
