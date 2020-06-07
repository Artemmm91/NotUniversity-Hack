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

from .forms import AuthForm, ImageForm, SignUpForm, RecoverForm, AddGoalForm, SearchForm, DeleteGoalForm
from .models import Avatar, ChooseGoals, Friends

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
            #goals = ChooseGoals.objects.filter(user=request.user)
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
        goals = ChooseGoals.objects.filter(user=request.user)
        image = str(image.img) if image is not None else 'web/static/avatars/default.png'
        context['avatar'] = image[11:]
        context['username'] = request.user.username
        context['goals'] = goals
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


@login_required
def adding_goal(request):
    if request.method == 'POST':
        form = AddGoalForm(request.POST)
        if form.is_valid():
            picked = form.cleaned_data.get('picked')
            level = form.cleaned_data.get('level')
            lst = ChooseGoals.objects.filter(user=request.user, goal=picked)
            if len(lst):
                lst = lst.first()
                lst.level = level
                lst.save()
            else:
                cg = ChooseGoals(user=request.user, goal=picked, level=level)
                cg.save()
            return redirect('/')
        else:
            return redirect('/')
    else:
        form = AddGoalForm()
        context = {'form': form}
        return render(request, 'web/add_goal.html', context)


def sign(x):
    if x == 0:
        return 0
    if x < 0:
        return -1
    return 1


def target_users(user0, lst):
    loc = [[abs(x.level - user0.level), -sign(x.level - user0.level), x] for x in lst]
    loc = sorted(loc)
    loc.remove([0, 0, user0])
    res = [x[2] for x in loc]
    return res[:min(len(res), 20)]


@login_required
def search_sport(request):
    context = {'ans': []}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            lst = ChooseGoals.objects.filter(user=request.user)
            picked = form.cleaned_data.get('search')
            if picked in [x.goal for x in lst]:
                lst_ans = target_users(ChooseGoals.objects.filter(goal=picked, user=request.user).first(), ChooseGoals.objects.filter(goal=picked))
                context['ans'] = lst_ans
                return render(request, 'web/find_sport.html', context)
            else:
                context['error'] = True
                return render(request, 'web/find_sport.html', context)
        else:
            return redirect('search/')
    else:
        form = SearchForm()
        context = {'form': form}
        return render(request, 'web/find_sport.html', context)


@login_required
def show_profile(request, id):
    context = {'id': id}
    lst = User.objects.filter(id=id)
    if not len(lst):
        context['error'] = True
        return redirect('/')
    target_user = lst.first()
    user_friends = Friends.object.filter(out_user=request.user)
    context['is_friend'] = target_user in user_friends
    context['friend'] = target_user
    return render(request, 'web/show_profile.html', context)


@login_required
def add_friend(request, id):
    lst = User.objects.filter(id=id)
    if not len(lst):
        return redirect('/')
    target_user = lst.first()
    user_friends = Friends.object.filter(out_user=request.user)
    if id != request.user.id and target_user not in user_friends:
        friendship = Friends(out_user=request.user, in_user=target_user)
        friendship.save()
    return redirect('profile/{}'.format(id))


@login_required
def delete_goal(request):
    if request.method == 'POST':
        form = DeleteGoalForm(request.POST)
        if form.is_valid():
            picked = form.cleaned_data.get('picked')
            lst = ChooseGoals.objects.filter(user=request.user, goal=picked)
            if len(lst):
                lst = lst.first()
                lst.delete()
            return redirect('../profile/')
        else:
            return redirect('../profile/')
    else:
        form = DeleteGoalForm()
        context = {'form': form}
        return render(request, 'web/delete_goal.html', context)
