#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.views import APIView

from .serializers import (
    CurrentUserDetailSerializer,
    ProfileRetrieveSerializer,
    UserLoginSerializer,
    UserSerializerWithToken,
)

User = get_user_model()


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = CurrentUserDetailSerializer(request.user, context={"request": request})
    return Response(serializer.data)


class UserSignUpAPIView(APIView):
    """
    View that handles user signup and returns username, email & JWT.
    """
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    """
    View that handles user login and returns username & JWT.
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProfileRetrieveAPIView(RetrieveAPIView):
    """
    View that returns user profile data.
    """
    queryset = User.objects.all()
    serializer_class = ProfileRetrieveSerializer
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
