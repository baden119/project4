import datetime
import json
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow

class NewPostForm(forms.Form):
    # Form to create a new post
    New_Post_Textfield = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Write something here', 'class': 'form-control'}))

def index(request):
    if request.user.is_authenticated:
        print(request.user.username)
        print("following:")
        for follow in request.user.follows.all():
            print(follow.followed)
        print("followers:")
        for follow in request.user.followers.all():
            print(follow.follower)
    all_posts = Post.objects.all().order_by('-timestamp')

    return render(request, "network/index.html", {
            "all_posts": all_posts,
            "NewPostForm": NewPostForm()
            })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    # Save a new post to the database
    # Validate form data.
    new_post_form = NewPostForm(request.POST)
    print(new_post_form)
    if new_post_form.is_valid():
        body = new_post_form.cleaned_data["New_Post_Textfield"]

    # Save post to database

    new_post = Post()
    new_post.user = request.user
    new_post.body = body
    new_post.save()

    return redirect('index')

def profile(request, username):
    # displays a users profile
    profile = User.objects.get(username=username)
    posts = profile.posts.all().order_by('-timestamp')

    # Determine if user is currently following the owner of the profile
    following = False
    if request.user.is_authenticated:
        for follow in request.user.follows.all():
            if follow.followed.username == username:
                following = True

    follows = len(profile.follows.all())
    followers = len(profile.followers.all())

    return render(request, "network/profile.html", {
            "username": username,
            "posts": posts,
            "following": following,
            "follows": follows,
            "followers": followers
            })

def follow(request, username):
    # Create new follow.
    new_follow = Follow()
    new_follow.follower = request.user
    new_follow.followed = User.objects.get(username=username)
    new_follow.save()
    return redirect(request.META["HTTP_REFERER"])

def unfollow(request, username):
    # Delete a follow.
    request.user.follows.get(followed = User.objects.get(username=username)).delete()
    return redirect(request.META["HTTP_REFERER"])

def following(request):
    # Display posts of followed users
    print(request.user.follows.all())

    posts = Post.objects.all()

    print(len(posts))
    return render(request, "network/following.html")
