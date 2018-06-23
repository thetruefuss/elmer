from datetime import timedelta

from django import template
from django.db.models import Count
from django.utils import timezone
from django.utils.safestring import mark_safe

import markdown

from ..models import Post

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
