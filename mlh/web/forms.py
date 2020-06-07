from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .sports import CHOICES


class AuthForm(forms.Form):
    username = forms.CharField(label='User', help_text='Your login')
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), help_text='Your password')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class RecoverForm(forms.Form):
    username = forms.CharField(label='User', help_text='Your login to recover your password')


class ImageForm(forms.Form):
    img = forms.ImageField(label='Avatar', help_text='Image for your avatar')


class AddGoalForm(forms.Form):
    picked = forms.ChoiceField(choices=CHOICES, required=True, label="Choose your goal sport", help_text='The sport you want to improve')
    level = forms.IntegerField(max_value=5, min_value=1, label="Choose your honest level in this sport")


class SearchForm(forms.Form):
    search = forms.ChoiceField(choices=CHOICES, required=True, label="Choose a sport you want to upgrade")


class DeleteGoalForm(forms.Form):
    picked = forms.ChoiceField(choices=CHOICES, required=True, label="Choose your goal, that you want to delete")


class AddPostForm(forms.Form):
    name = forms.CharField(label='How would you like to name your post?')
    text = forms.CharField(label='What would you like to post today?')
