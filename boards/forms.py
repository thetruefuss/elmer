from django import forms

from .models import Board


class BoardForm(forms.ModelForm):
    """
    Form that handles board data.
    """
    class Meta:
        model = Board
        fields = ('title', 'description', 'cover')
