import datetime
import json
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import User, Post, Follow, Like

class NewPostForm(forms.Form):
    # Form to create a new post
    New_Post_Textfield = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Write something here', 'class': 'form-control'}))

def like_data_loader(request, posts):

     # Each Post contains two fields, 'is_liked_by_current_user' and 'total_likes' which are intended to be modified
     # dynamically with the following statements. This information is passed to the HTML template and necessary for
     # the Like/Unlike functionality.
    for post in posts:
        post.total_likes = (len(post.likes.all()))
        if request.user.is_authenticated:
            for liked_post in request.user.likes.all():
                if post.id == liked_post.post_id:
                    post.is_liked_by_current_user = True

    return posts

def get_timestamp(post):
    # Function to help with sorting a list of posts from multiple database queries, sourced from:
    # https://www.programiz.com/python-programming/methods/list/sort
    return(post.timestamp)

def pagination_helper(request, posts):
    # pagination syntax taken from:
    # https://codeloop.org/django-pagination-complete-example/
    paginated = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginated.page(page)
    except PageNotAnInteger:
        posts = paginated.page(1)
    except EmptyPage:
        posts = paginated.page(paginated.num_pages)

    pagination_data = {
        "posts": posts,
        "page": page
    }

    return pagination_data

def index(request):
    # Displays all posts
    posts = Post.objects.all().order_by('-timestamp')

    # Each post needs additional 'like' data loaded into it dynamically using the like_data_loader function.
    like_data_loader(request, posts)

    # Display pages in a paginated fashion.
    pagination_data = pagination_helper(request, posts)

    return render(request, "network/index.html", {
            "posts": pagination_data["posts"],
            "page": pagination_data["page"],
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
    # View a users profile
    profile = User.objects.get(username=username)
    posts = profile.posts.all().order_by('-timestamp')

    # Each post needs additional 'like' data loaded into it dynamically using the like_data_loader function.
    like_data_loader(request, posts)

    # Display pages in a paginated fashion.
    pagination_data = pagination_helper(request, posts)

    # Determine if current user is following of the profile being viewed
    following = False
    if request.user.is_authenticated:
        for follow in request.user.follows.all():
            if follow.followed.username == username:
                following = True

    # For the profile being viewed, count the followers and follows.
    follows = len(profile.follows.all())
    followers = len(profile.followers.all())


    return render(request, "network/profile.html", {
            "username": username,
            "posts": pagination_data["posts"],
            "page": pagination_data["page"],
            "following": following,
            "follows": follows,
            "followers": followers,
            "NewPostForm": NewPostForm()
            })

def follow(request, username):
    # When the current user follows another user, a new 'Follow' object needs to be created in the database.

    # Create new follow.
    new_follow = Follow()
    new_follow.follower = request.user
    new_follow.followed = User.objects.get(username=username)
    new_follow.save()
    return redirect(request.META["HTTP_REFERER"])

def unfollow(request, username):
    # When the current user choses to stop following another user, the 'Follow' object needs to be deleted from the database.

    # Delete a follow.
    request.user.follows.get(followed = User.objects.get(username=username)).delete()
    return redirect(request.META["HTTP_REFERER"])

def following(request):
    # Display all posts by users being followed by the current user

    posts = []
    for user in request.user.follows.all():
        for post in Post.objects.filter(user=user.followed):
            posts.append(post)

    # To chronologically sort a list containing from multiple seperate database queries, a simple function is employed (get_timestamp).
    posts.sort(key=get_timestamp, reverse=True)

    # Each post needs additional 'like' data loaded into it dynamically using the like_data_loader function.
    like_data_loader(request, posts)

    # Display pages in a paginated fashion.
    pagination_data = pagination_helper(request, posts)

    return render(request, "network/following.html", {
        "following": len(request.user.follows.all()),
        "posts": pagination_data["posts"],
        "page": pagination_data["page"]
    })

def edit_post(request):
    # Reached via Fetch request, this function saves edited post data.

    # Edit request must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Parse data from POST request
    data = json.loads(request.body)
    post_body = data["post_body"]
    post_id = data["post_id"]

    # Save data to database
    post = Post.objects.get(pk=post_id)
    post.body = post_body
    post.save()

    # Send response to Fetch request containing newly saved post data.
    return JsonResponse({"message": "Email sent successfully.", "post_body": post_body}, status=201)

def like_post(request):
    # Reached via Fetch request, this allows a user to like a post by creating a 'Like' object in the database.
    # It also allows a user to un-like a post by deleting 'Like' objects from the database.

    # Like request must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Parse data from POST request
    data = json.loads(request.body)
    post_id = data["post_id"]

    # Look for a 'Like' object in the database between containing current user and the requested post.
    like_query = Like.objects.filter(post=Post.objects.get(pk=post_id), user=request.user)

    # "exists()" technique sourced from:
    # https://stackoverflow.com/questions/40910149/django-exists-versus-doesnotexist
    if like_query.exists():
        # Delete Like
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

    # Count the new total likes for the post, which will be automatically updated in HTML
    like_count = len(Post.objects.get(pk=post_id).likes.all())

    return JsonResponse({"message": message, "like_condition": like_condition, "like_count": like_count}, status=201)
