from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators  import login_required

from .models import Friend, FriendRequest, Posts, Comments, Profile
from .forms import AccountForm, PostForm

from django.http import HttpResponse


def get_recent_posts(user):
    if user.is_authenticated:
        friends_list = Friend.objects.friends(user)
        qs = Posts.objects.filter(author__in=friends_list) | Posts.objects.filter(author=user)
        return qs.order_by('-created_at')

def index(request):

    if request.user.is_authenticated:
        friends_list = Friend.objects.friends(request.user)
        if friends_list:
            news_feed = get_recent_posts(request.user)
            context = {'friends': friends_list, 'news_feed': news_feed}
            return render(request, 'site/index.html', context)
        else:
            return render(request, 'site/index.html')
    else:
        return render(request, 'site/index.html')

def account_logout(request):
    logout(request)

    return redirect('index')

@login_required(login_url='/')
def profile(request, username):
    profile = Profile.objects.filter(user__username=username)
    args = {'profile': profile}
    return render(request, 'site/profile.html', args)

def view_post(request, post_id):
    return HttpResponse("This is the post %s" % post_id)

def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        else:
            return HttpResponse("Error")

def post_comments(request, post_id):
    post = Posts.objects.get(pk=post_id)
    comments = post.get_comments()
    return render(request, 'site/comments.html', {'c':comments})
def account_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse("Your Account is disabled.")
        else:
            return HttpResponse("Invalid Credentials.")

def account_signup(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            Profile.objects.create(user=user)
            Friend.objects.create(user=user)
            return redirect('index')
    else:
        return redirect('index')
