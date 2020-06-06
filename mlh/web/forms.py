from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AuthForm(forms.Form):
    username = forms.CharField(label='User')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class RecoverForm(forms.Form):
    username = forms.CharField(label='User')


class ImageForm(forms.Form):
    img = forms.ImageField(label='Avatar')


CHOICES = (
    ('a', 'Running'),
    ('b', 'Swimming'),
    ('c', 'Light athletics'),
    ('d', 'Heavy athletics'),
)


class AddGoalForm(forms.Form):
    picked = forms.ChoiceField(choices=CHOICES, required=True)
    level = forms.IntegerField(label='Level', max_value=5, min_value=1)