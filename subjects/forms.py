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

    title = forms.CharField(help_text="You can mention other members in your post i.e <b>u/username</b>")
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    board = forms.ModelChoiceField(queryset=Board.objects.all())

    def __init__(self, *args, **kwargs):
        """
        Initialize the form by populating board options with
        user's subscribed boards.
        """
        user = kwargs.pop('user', None)
        super(SubjectForm, self).__init__(*args, **kwargs)
        if user is not None:
            subscribed_boards = user.subscribed_boards.all()
            self.fields['board'].queryset = subscribed_boards
            if not subscribed_boards:
                self.fields['board'].help_text = "You need to <b>subscribe</b> a board to post in it."

    class Meta:
        model = Subject
        fields = ('title', 'body', 'photo', 'board')
