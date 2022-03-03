from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.db import transaction

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from socialnetwork.forms import LoginForm, RegisterForm, PostForm, ProfileForm
from socialnetwork.models import Entry, Post, Profile


def login_action(request):
    if request.method == 'GET':
        l = LoginForm()
        context = {'form': l}
        return render(request, 'socialnetwork/login.html', context)

    form = LoginForm(request.POST)
    context = {'form': form}

    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('global'))

def logout_action(request):
    logout(request)
    return render(request, 'socialnetwork/login.html', {'form': LoginForm()})

def register_action(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    form = RegisterForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    new_user = User.objects.create_user(
        username = form.cleaned_data['username'],
        password = form.cleaned_data['password'],
        email = form.cleaned_data['email'],
        first_name = form.cleaned_data['first_name'],
        last_name = form.cleaned_data['last_name']
    )

    new_profile = Profile()
    new_profile.user = new_user
    new_profile.save()

    new_user.save()
    new_user = authenticate(username = form.cleaned_data['username'],
                            password = form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('global'))

@login_required(login_url='/socialnetwork/login')
def global_action(request):
    if request.method == 'GET':
        return  render(request, 'socialnetwork/global.html', {'posts': Post.objects.all().order_by('-creation_time')})
    if 'text' not in request.POST or not request.POST['text']:
        return render(request, 'socialnetwork/global.html', {'posts': Post.objects.all().order_by('-creation_time'), 'error': 'Post cannot be blank'})

    new_post = Post(text = request.POST['text'], user = request.user, creation_time = timezone.now())
    new_post.save()
    return  render(request, 'socialnetwork/global.html', {'posts': Post.objects.all().order_by('-creation_time')})

@login_required
def profile_action(request):
    if request.method == 'GET':
        context = {'profile': request.user.profile,
                   'form': ProfileForm(initial={'bio_text': request.user.profile.bio_text})}
        return render(request, 'socialnetwork/profile.html', context)
    form = ProfileForm(request.POST, request.FILES)
    if not form.is_valid():
        context = {'profile': request.user.profile,
                   'form': form}
        return render(request, 'socialnetwork/profile.html', context)
    pic = form.cleaned_data['picture']
    request.user.profile.picture = pic
    request.user.profile.bio_text = form.cleaned_data['bio_text']
    request.user.profile.content_type = pic.content_type
    request.user.profile.save()
    context = {'profile': request.user.profile,
               'form': form}
    return render(request, 'socialnetwork/profile.html', context)

@login_required
def other_action(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'socialnetwork/other.html', {'profile': user.profile})

@login_required
def follower_action(request):
    if request.method == 'GET':
        return  render(request, 'socialnetwork/follower.html', {'posts': Post.objects.all().order_by('-creation_time')})
    return  render(request, 'socialnetwork/follower.html', {'posts': Post.objects.all().order_by('-creation_time')})

@login_required
def unfollow_action(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    return render(request, 'socialnetwork/other.html', {'profile': user_to_unfollow.profile})

@login_required
def follow_action(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()
    return render(request, 'socialnetwork/other.html', {'profile': user_to_follow.profile})

@login_required
def photo_action(request, user_id):
    item = get_object_or_404(Profile, id=user_id)
    print('Picture #{} fetched from db: {} (type={})'.format(user_id, item.picture, type(item.picture)))

    if not item.picture:
        raise Http404

    return HttpResponse(item.picture, content_type=item.content_type)