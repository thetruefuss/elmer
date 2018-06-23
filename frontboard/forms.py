from django import forms

from .models import Board, Comment, Subject


class SubjectForm(forms.ModelForm):
    def get_subscribed_boards(self):
        return self.user.subscribed_boards

    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'maxlength': 150,
                                                                         'placeholder': 'Title your subject'}))
    body = forms.CharField(label='Description', required=False,
                           widget=forms.Textarea(attrs={'placeholder': 'Describe your subject'}))
    board = forms.ModelChoiceField(label='Board', queryset=Board.objects.all(), empty_label='Select Board')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SubjectForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['board'].queryset = user.subscribed_boards.all()

    class Meta:
        model = Subject
        fields = ('title', 'body', 'photo', 'board')


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Type your message here',
                                                                  'rows': '3'}))

    class Meta:
        model = Comment
        fields = {'body'}


class ReplyForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Type your reply',
                                                                  'rows': '3'}))

    class Meta:
        model = Comment
        fields = {'body'}


class BoardForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 500}))

    class Meta:
        model = Board
        fields = ('title', 'description', 'cover')
