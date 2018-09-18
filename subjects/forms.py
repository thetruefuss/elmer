from django import forms

from boards.models import Board

from .models import Subject


class SubjectForm(forms.ModelForm):
    """
    Form that handles subject data.
    """
    def get_subscribed_boards(self):
        """Return a list of user's subscribed boards."""
        return self.user.subscribed_boards

    board = forms.ModelChoiceField(queryset=Board.objects.all())

    def __init__(self, *args, **kwargs):
        """
        Initialize the form by populating board options with
        user's subscribed boards.
        """
        user = kwargs.pop('user', None)
        super(SubjectForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['board'].queryset = user.subscribed_boards.all()

    class Meta:
        model = Subject
        fields = ('title', 'body', 'photo', 'board')
