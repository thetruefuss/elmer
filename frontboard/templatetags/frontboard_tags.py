import random

from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

import markdown

from ..models import Board

register = template.Library()


@register.inclusion_tag('includes/boards_container.html')
def boards_container_items(user):
    """
    Returns a dict containing user & user's subscribed boards.

    :param filename: Object
    :return: dict
    """
    boards_list = user.subscribed_boards.all()
    return {'boards_list': boards_list, 'user': user}


@register.filter(name='markdown')
def markdown_format(text):
    """
    Markdown the text.

    :param text: string
    :return: string
    """
    return mark_safe(markdown.markdown(text))


def top_boards():
    """
    Returns a list of top five boards based on number of recent posts in them.

    :return: list
    """
    boardslist = Board.objects.all()
    boardslist = sorted(boardslist, key=lambda instance: instance.recent_posts(), reverse=True)[:5]
    return boardslist


@register.inclusion_tag('includes/top_five.html')
def top_five_boards():
    """
    Returns a dict containing top five boards list.

    :return: dict
    """
    return {'boards_list': top_boards(), 'top_boards': True}


@register.inclusion_tag('includes/active_threads.html')
def show_active_threads(user):
    """
    Returns a dict containing user active threads.

    :param user: Object
    :return: dict
    """
    current_user = User.objects.get(id=user.id)
    threads = current_user.posted_subjects.all()[:5]
    return {'threads': threads}


@register.inclusion_tag('includes/suggested_users.html')
def show_suggested_users(user):
    """
    Returns a dict containing a list of five suggested (random) users.

    :param user: Object
    :return: dict
    """
    current_user = User.objects.get(id=user.id)
    # users_nts: USERS NOT TO SUGGEST
    users_nts = [follower.user.username for follower in current_user.following.all()]
    users_nts.append(current_user.username)
    # users_ts: USERS TO SUGGEST
    users_ts = User.objects.exclude(username__in=users_nts)
    NUM_OF_SUGGESTED_USERS = 5
    if len(users_ts) >= NUM_OF_SUGGESTED_USERS:
        users_list = random.sample(list(users_ts), NUM_OF_SUGGESTED_USERS)
    else:
        num_of_users = len(users_ts)
        users_list = random.sample(list(users_ts), num_of_users)
    return {'users_list': users_list, 'current_user': current_user}
