from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UpdateUserForm, UpdateUserProfileForm, PostForm, CommentForm
from django.contrib.auth import login, authenticate
from .models import Post, Comment, Profile, Follow
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.generic import RedirectView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='login')
def index(request):
    images = Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
    parameters = {
        'images': images,
        'form': form,
        'users': users,

    }
    return render(request, 'instagram/index.html', parameters)


@login_required(login_url='login')
def profile(request, username):
    images = request.user.profile.posts.all()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.profile)
    parameters = {
        'user_form': user_form,
        'profile_form': profile_form,
        'images': images,

    }
    return render(request, 'instagram/profile.html', parameters)


@login_required(login_url='login')
def profileUser(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == profileUser:
        return redirect('profile', username=request.user.username)
    user_posts = profileUser.profile.posts.all()
    
    followers = Follow.objects.filter(followed=profileUser.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    parameters = {
        'profileUser': profileUser,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    print(followers)
    return render(request, 'instagram/profileUser.html', parameters)


@login_required(login_url='login')
def post_comment(request, id):
    image = get_object_or_404(Post, pk=id)
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            savecomment = form.save(commit=False)
            savecomment.post = image
            savecomment.user = request.user.profile
            savecomment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    parameters = {
        'image': image,
        'form': form,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    return render(request, 'instagram/post.html', parameters)


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs.get('id')
        print(id)
        obj = get_object_or_404(Post, pk=id)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user in obj.likes.all():
            obj.likes.remove(user)
        else:
            obj.likes.add(user)
        return url_


class PostLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None, format=None):
        # id = self.kwargs.get('id')
        obj = get_object_or_404(Post, pk=id)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user in obj.likes.all():
            liked = False
            obj.likes.remove(user)
        else:
            liked = True
            obj.likes.add(user)
        updated = True
        data = {

            'updated': updated,
            'liked': liked,
        }
        print(data)
        return Response(data)


def like_post(request):
    image = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        image.likes.remove(request.user)
        is_liked = False
    else:
        image.likes.add(request.user)
        is_liked = False

    parameters = {
        'image': image,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    if request.is_ajax():
        html = render_to_string('instagram/like.html', parameters, request=request)
        return JsonResponse({'form': html})


@login_required(login_url='login')
def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Profile.search_profile(name)
        print(results)
        message = f'name'
        parameters = {
            'results': results,
            'message': message
        }
        return render(request, 'instagram/search.html', parameters)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'instagram/search.html', {'message': message})


def unfollow(request, to_unfollow):
    if request.method == 'GET':
        profileUser2 = Profile.objects.get(pk=to_unfollow)
        unfollow_d = Follow.objects.filter(follower=request.user.profile, followed=profileUser2)
        unfollow_d.delete()
        return redirect('profileUser', profileUser2.user.username)


def follow(request, to_follow):
    if request.method == 'GET':
        profileUser3 = Profile.objects.get(pk=to_follow)
        follow_s = Follow(follower=request.user.profile, followed=profileUser3)
        follow_s.save()
        return redirect('profileUser', profileUser3.user.username)
