#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms

from .models import Board


class BoardForm(forms.ModelForm):
    """
    Form that handles board data.
    """
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    cover = forms.ImageField(widget=forms.FileInput(),
                             help_text="Image dimensions should be <b>900 &#10005; 300</b>.",
                             required=False)

    class Meta:
        model = Board
        fields = ('title', 'description', 'cover')
