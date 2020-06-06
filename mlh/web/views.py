from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import os
from string import ascii_letters, digits

from .forms import AuthForm, ImageForm, SignUpForm, RecoverForm
from .models import Avatar

# Create your views here.


def index(request):
    return render(request, 'web/index.html')


def login_view(request):
    context = {}
    if request.POST:
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.data['username'], password=form.data['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/signin')
        else:
            return redirect('/signin')
    else:
        form = AuthForm()
        context['auth_form'] = form
        return render(request, 'web/auth.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def add_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'web/sign_up.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/')
        else:
            return redirect('profile/new_pass')
    else:
        form = PasswordChangeForm(request)
        context = {'form': form}
        return render(request, 'web/new_pass.html', context)


@login_required
def user_profile(request):
    context = {}
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = Avatar.objects.filter(user=request.user).first()
            if image is not None:
                if str(image.img) != 'mlh/web/static/avatars/default.png':
                    os.remove(str(image.img))
            else:
                image = Avatar(user=request.user)
            image.img = form.cleaned_data['img']
            image.save()
            return redirect('/profile')
        else:
            return redirect('/profile')
    else:
        image = Avatar.objects.filter(user=request.user).first()
        image = str(image.img) if image is not None else 'mlh/web/static/avatars/default.png'
        context['avatar'] = image[15:]
        context['username'] = request.user.username
        return render(request, 'web/user_profile.html', context)


def reset_password(request):
    context = {}
    if request.method == 'POST':
        form = RecoverForm(request.POST)
        if form.is_valid():
            name = form.data['username']
            u = User.objects.filter(username=name).first()
            if u is not None:
                new_password = User.objects.make_random_password(length=10, allowed_chars=ascii_letters + digits)
                u.set_password(new_password)
                u.save()
                message = 'Hi! Your new password is: ' + new_password
                mail = u.email
                send_mail('New Password', message, 'from@example.com', [mail])
                return redirect('/')
            else:
                redirect('/')
        else:
            return redirect('signin/')
    else:
        form = RecoverForm()
        context['name_form'] = form
    return render(request, 'web/rec_pass.html', context)
