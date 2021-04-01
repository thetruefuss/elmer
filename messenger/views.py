#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from mysite.decorators import ajax_required

from .models import Message


@login_required
def inbox(request):
    """
    Displays an inbox page of user.
    """
    conversations = Message.get_conversations(user=request.user)
    users_list = request.user.profile.contact_list.all().filter(is_active=True)

    never_send_msg = True

    return render(request, 'messenger/inbox.html', {
        'conversations': conversations,
        'users_list': users_list,
        'never_send_msg': never_send_msg
    })


@login_required
def messages(request, username):
    """
    Displays message threads of user.
    """
    user = User.objects.get(username=username)

    if request.user in user.profile.contact_list.all():
        conversations = Message.get_conversations(user=request.user)
        users_list = request.user.profile.contact_list.all().filter(is_active=True)
        active_conversation = username
        chat_msgs = Message.objects.filter(user=request.user, conversation__username=username)
        chat_msgs.update(is_read=True)

        for conversation in conversations:
            if conversation['user'].username == username:
                conversation['unread'] = 0

        return render(
            request, 'messenger/inbox.html', {
                'chat_msgs': chat_msgs,
                'conversations': conversations,
                'users_list': users_list,
                'active': active_conversation
            })
    else:
        return HttpResponse('')


@login_required
@ajax_required
def load_new_messages(request):
    """
    Loads new messages via ajax.
    """
    last_message_id = request.GET.get('last_message_id')
    username = request.GET.get('username')
    user = User.objects.get(username=username)

    if request.user in user.profile.contact_list.all():
        chat_msgs = Message.objects.filter(user=request.user, conversation__username=username,
                                           id__gt=last_message_id).exclude(from_user=request.user)
        if chat_msgs:
            chat_msgs.update(is_read=True)
            return render(request, 'messenger/includes/partial_load_more_messages.html', {'chat_msgs': chat_msgs})
        else:
            return HttpResponse('')


@login_required
@ajax_required
def load_last_twenty_messages(request):
    load_from_msg_id = request.GET.get('load_from_msg_id')
    username = request.GET.get('username')
    user = User.objects.get(username=username)
    if request.user in user.profile.contact_list.all():
        chat_msgs = Message.objects.filter(user=request.user, conversation__username=username, id__lt=load_from_msg_id)
        if chat_msgs:
            chat_msgs.update(is_read=True)
            return render(request, 'messenger/includes/partial_load_more_messages.html', {'chat_msgs': chat_msgs})
        else:
            return HttpResponse('')


@login_required
@ajax_required
def delete(request):
    return HttpResponse()


@login_required
@ajax_required
def send(request):
    """
    Handles the message send action.
    """
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return HttpResponse()

        if from_user != to_user:
            chat_msg = Message.send_message(from_user, to_user, message)
            return render(request, 'messenger/includes/partial_message.html', {'chat_msg': chat_msg})
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@login_required
@ajax_required
def check(request):
    """
    Checks for new messages.
    """
    count = Message.objects.filter(user=request.user, is_read=False).count()
    return HttpResponse(count)
