import json
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import NewPost

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

def index(request):

    post_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj,
    })

@csrf_exempt
@login_required
def add_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    text = data.get("body")

    post = Post(
        user=request.user,
        text=text
    )
    post.save()

    return JsonResponse({"message": "Posted successfully."}, status=201)

@csrf_exempt
@login_required
def post(request, post_id):

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialise())

    elif request.method == "PATCH":
        data = json.loads(request.body)
        text = data.get("body")

        post = Post.objects.get(pk=post_id)
        post.text = text
        post.save()
        return JsonResponse({"message": "Edited successfully."}, status=201)
        
    else:
        return JsonResponse({
            "error": "GET or PUT or PATCH request required."
        }, status=400)

def profile(request, username):

    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by("-timestamp")
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    follower_count = User.objects.all().filter(following=user.id).count()

    following_count = User.objects.all().filter(followers=user.id).count()

    return render(request, "network/profile.html", {
        "page_obj": page_obj, 
        "profile": user,
        "follower_count": follower_count,
        "following_count": following_count
    })

@csrf_exempt
@login_required
def like(request):
    
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post_id") is not None and data.get("user_id") is not None:
            post_id = data.get("post_id")
            user_id = data.get("user_id")
            try:
                post = Post.objects.get(pk=post_id)
                user = User.objects.get(pk=user_id)
                userLiked = post.likes.all().filter(pk=user_id).exists()

                if userLiked:
                    post.likes.remove(user)
                    user.likes.remove(post)
                else:
                    post.likes.add(user)
                    user.likes.add(post)
                post.save()
                user.save()
                return JsonResponse(post.serialise())
            except:
                return JsonResponse({'error': "Post not found", "status": 404})
    return JsonResponse({}, status=400)

@csrf_exempt
@login_required
def follow(request):

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("user_id") is not None and data.get("current") is not None:
            user_id = data.get("user_id")

            try:
                user = User.objects.get(pk=user_id)
                current = request.user
                following = user.followers.all().filter(pk=current.id).exists()

                if following:
                    user.followers.remove(current)
                    user.save()
                    return JsonResponse({"message": "Unfollowed"}, status=201)
                else:
                    user.followers.add(current)
                    user.save()
                    return JsonResponse({"message": "Followed"}, status=201)
            except:
                return JsonResponse({'error': "Something went wrong", "status": 404})
    return JsonResponse({}, status=400)

@login_required
def following(request, username):

    posts = []

    user = User.objects.get(username=username)
    followers = User.objects.all().filter(followers=user)

    for follow in followers:
        posts_list = list(Post.objects.filter(user=follow).order_by("-timestamp"))
        for post in posts_list: 
            posts.append(post)

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "user": user,
        "page_obj": page_obj,
    })