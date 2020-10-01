import datetime
import json
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow, Like

class NewPostForm(forms.Form):
    # Form to create a new post
    New_Post_Textfield = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Write something here', 'class': 'form-control'}))

def index(request):
    # Displays all posts
    all_posts = Post.objects.all().order_by('-timestamp')

     # Each Post contains two fields, 'is_liked_by_current_user' and 'total_likes' which are intended to be modified
     # dynamically with the following statements. This information is passed to the HTML template and necessary for
     # the Like/Unlike functionality.
    for post in all_posts:
        post.total_likes = (len(post.likes.all()))
        if request.user.is_authenticated:
            for liked_post in request.user.likes.all():
                if post.id == liked_post.post_id:
                    post.is_liked_by_current_user = True

    paginated = Paginator(all_posts, 10)

    # pagination syntax taken from:
    # https://codeloop.org/django-pagination-complete-example/
    page = request.GET.get('page')
    try:
        posts = paginated.page(page)
    except PageNotAnInteger:
        posts = paginated.page(1)
    except EmptyPage:
        posts = paginated.page(paginated.num_pages)

    print_hello("network/index.html")

    return render(request, "network/index.html", {
            "posts": posts,
            "page": page,
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
    if new_post_form.is_valid():
        body = new_post_form.cleaned_data["New_Post_Textfield"]

    # Save post to database
    new_post = Post()
    new_post.user = request.user
    new_post.body = body
    new_post.save()

    # Automatically Like your own post
    new_like = Like()
    new_like.post = Post.objects.get(pk=new_post.pk)
    new_like.user = request.user
    new_like.save()

    return redirect('index')

def profile(request, username):
    # displays a users profile
    profile = User.objects.get(username=username)
    paginated = Paginator(profile.posts.all().order_by('-timestamp'), 10)
    # posts = profile.posts.all().order_by('-timestamp')

    # Determine if user is currently following the owner of the profile
    following = False
    if request.user.is_authenticated:
        for follow in request.user.follows.all():
            if follow.followed.username == username:
                following = True

    follows = len(profile.follows.all())
    followers = len(profile.followers.all())


    # pagination syntax taken from:
    # https://codeloop.org/django-pagination-complete-example/
    page = request.GET.get('page')
    try:
        posts = paginated.page(page)
    except PageNotAnInteger:
        posts = paginated.page(1)
    except EmptyPage:
        posts = paginated.page(paginated.num_pages)

    print_hello("network/profile.html")
    return render(request, "network/profile.html", {
            "username": username,
            "page": page,
            "posts": posts,
            "following": following,
            "follows": follows,
            "followers": followers,
            "NewPostForm": NewPostForm()
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

    # Functoion to help with sorting posts, taken from:
    # https://www.programiz.com/python-programming/methods/list/sort
    def get_timestamp(post):
        return(post.timestamp)

    posts = []
    for user in request.user.follows.all():
        for post in Post.objects.filter(user=user.followed):
            posts.append(post)

    posts.sort(key=get_timestamp, reverse=True)
    paginated = Paginator(posts, 10)

    # pagination syntax taken from:
    # https://codeloop.org/django-pagination-complete-example/
    page = request.GET.get('page')
    try:
        posts = paginated.page(page)
    except PageNotAnInteger:
        posts = paginated.page(1)
    except EmptyPage:
        posts = paginated.page(paginated.num_pages)

    print_hello("network/following.html")

    return render(request, "network/following.html", {
        "following": len(request.user.follows.all()),
        "page": page,
        "posts": posts
    })

def edit_post(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post_body = data["post_body"]
    post_id = data["post_id"]

    post = Post.objects.get(pk=post_id)
    post.body = post_body
    post.save()

    return JsonResponse({"message": "Email sent successfully.", "post_body": post_body}, status=201)

def like_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post_id = data["post_id"]

    # "exists()" technique sourced from:
    # https://stackoverflow.com/questions/40910149/django-exists-versus-doesnotexist

    like_query = Like.objects.filter(post=Post.objects.get(pk=post_id), user=request.user)

    if like_query.exists():
        # Delete LIKE
        request.user.likes.get(post = Post.objects.get(pk=post_id)).delete()
        like_condition = False
        message = "Post Un-Liked"

    else:
        # Create Like
        new_like = Like()
        new_like.post = Post.objects.get(pk=post_id)
        new_like.user = request.user
        new_like.save()
        like_condition = True
        message = "Post Liked"

    like_count = len(Post.objects.get(pk=post_id).likes.all())
    return JsonResponse({"message": message, "like_condition": like_condition, "like_count": like_count}, status=201)

def print_hello(route):

    print("hello!")
    print(route)

    return
