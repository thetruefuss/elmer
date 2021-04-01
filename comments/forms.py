#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form that handles comment data.
    """
    class Meta:
        model = Comment
        fields = ('body', )
