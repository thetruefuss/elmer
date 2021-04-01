#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from messenger.models import Message

from .serializers import ContactsListSerializer, MessageListSerializer


class ContactsListAPIView(ListAPIView):
    """
    View that returns user's contact list.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ContactsListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = self.request.user.profile.contact_list.all().filter(is_active=True)
        return queryset_list


class MessageListAPIView(ListAPIView):
    """
    View that returns coversation between two users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageListSerializer

    def get_queryset(self, *args, **kwargs):
        username = self.request.GET.get('username', '')
        queryset_list = Message.objects.filter(user=self.request.user, conversation__username=username)
        queryset_list.update(is_read=True)
        return queryset_list


class MessageCreateAPIView(APIView):
    """
    View that handles the creation of messages.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        to_user_username = data.get('to')
        message = data.get('message')

        from_user = self.request.user
        to_user = User.objects.filter(username=to_user_username)
        if to_user.count() == 1:
            if from_user != to_user:
                chat_msg = Message.send_message(from_user, to_user, message)
            # Return data serialized using new MessageSerializer
            return Response({"to": to_user, "message": message})
        return Response({"detail": "User does not exists."}, status=401)
