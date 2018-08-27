import random
from datetime import timedelta

from django import template
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from django.utils.safestring import mark_safe

import markdown
from cache_memoize import cache_memoize

from ..models import Board

register = template.Library()


@register.inclusion_tag('includes/boards_container.html')
def boards_container_items(user):
    boards_list = user.subscribed_boards.all()
    return {'boards_list': boards_list, 'user': user}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


def top_boards():
    boardslist = Board.objects.all()
    boardslist = sorted(boardslist, key=lambda instance:instance.recent_posts(), reverse=True)[:5]
    return boardslist


@register.inclusion_tag('includes/top_five.html')
def top_five_boards():
    return {'boards_list':top_boards(),'top_subjects':True}


@register.inclusion_tag('includes/active_threads.html')
def show_active_threads(user):
    current_user = User.objects.get(id=user.id)
    threads = current_user.posted_subjects.all()[:5]
    return {'threads': threads}


@register.inclusion_tag('includes/suggested_users.html')
def show_suggested_users(user):
    current_user = User.objects.get(id=user.id)
    users_not_to_render = [u.user.username for u in current_user.following.all()]
    users_not_to_render.append(current_user.username)
    users_list = User.objects.exclude(username__in=users_not_to_render)
    NUM_OF_SU = 5
    if len(users_list) >= NUM_OF_SU:
        users_list=random.sample(list(users_list), NUM_OF_SU)
    else:
        num_of_users = len(users_list)
        users_list = random.sample(list(users_list), num_of_users)
    return {'users_list': users_list, 'current_user': current_user}
