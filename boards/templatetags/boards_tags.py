import random

from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

import markdown

from ..models import Board

register = template.Library()


@register.inclusion_tag('includes/boards_container.html')
def boards_container_items(user):
    """Returns a dict containing user & user's subscribed boards."""
    boards_list = user.subscribed_boards.all()
    return {'boards_list': boards_list, 'user': user}


@register.inclusion_tag('includes/top_five.html')
def top_five_boards():
    """Returns a dict containing top five boards list."""
    boardslist = Board.objects.all()
    boardslist = sorted(boardslist, key=lambda instance: instance.recent_posts(), reverse=True)[:5]
    return {'boards_list': boardslist, 'top_boards': True}


@register.filter(name='markdown')
def markdown_format(text):
    """Markdown the text."""
    return mark_safe(markdown.markdown(text))


@register.inclusion_tag('includes/active_threads.html')
def show_active_threads(user):
    """Returns a dict containing user active threads."""
    current_user = User.objects.get(id=user.id)
    threads = current_user.posted_subjects.all()[:5]
    return {'threads': threads}
