from django import forms
from django.contrib.auth.models import User

from .models import Profile


class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'maxlength': 150}))
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    dob = forms.CharField(label="Date of Birth", widget=forms.TextInput(attrs={'placeholder': 'y-m-d',
                                                                               'maxlength': 150}))

    class Meta:
        model = Profile
        fields = ('dob', 'dp')
