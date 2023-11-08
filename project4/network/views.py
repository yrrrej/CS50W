import json
from typing import Type
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from network.models import Like,Post,Follow,Followers
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


@csrf_exempt
def index(request):
    posts=Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    paginator=Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method=='POST' and 'postbutton' in request.POST:
        body=request.POST["contents"]
        newpost=Post.objects.create(user=request.user,content=body)

    elif request.method == "PUT":
        data = json.loads(request.body)
        post=Post.objects.get(pk=data['post_id'])
        post.content=data['content']
        post.save()

    return render(request,'network/index.html',{
        'posts': posts,
        'page_obj': page_obj
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
        Follow.objects.create(user=request.user)
        Followers.objects.create(user=request.user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def addlikebyuser(request,posts):
    test=[]
    for i in posts:
        if request.user.is_authenticated:
            if i.likes.filter(user=request.user,post=i.id):
                new=i.serailize()
                new['likebyuser']='yes'
                test.append(new)
            else:
                new=i.serailize()
                new['likebyuser']='no'
                test.append(new)
        else:
            new=i.serailize()
            new['likebyuser']='notloggedin'
            test.append(new)

        new['ownpost']=(request.user==i.user)
    return test

def posts(request):
    posts=Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    
    return JsonResponse(addlikebyuser(request,posts), safe=False)

def likes(request,post_id):
    post=Post.objects.get(pk=post_id)
    try:
        userlikes=Like.objects.get(user=request.user)
    except Like.DoesNotExist:
        post.likes.create(user=request.user)

    #check if user liked this post or not
    userlikes=Like.objects.get(user=request.user)
    if post in userlikes.post.all():
        userlikes.post.remove(post)

    else:
        userlikes.post.add(post)

    return JsonResponse(addlikebyuser(request,[post]),safe=False)


def profileAPI(request,user_id):
    posts=Post.objects.filter(user=user_id)
    return JsonResponse(addlikebyuser(request,posts),safe=False)

def profile(request,username):
    who=User.objects.get(username=username)
    posts=Post.objects.filter(user=who.id)
    posts = posts.order_by("-timestamp").all()
    paginator=Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        userfollowing=Follow.objects.get(user=request.user)
    except Follow.DoesNotExist:
        Follow.objects.create(user=request.user)
    except TypeError:
        return render(request,'network/profile.html',{
        'username':who.username,
        'user_id':who.id,
        'following':who.follower.count(),
        'follower':who.following.count(),
        'button': 'Follow',
        'posts': posts,
        'lookingatown': who.username==request.user.username,
        'page_obj': page_obj
    })

    try:
        whofollower=Followers.objects.get(user=who)
    except Followers.DoesNotExist:
        Followers.objects.create(user=who)
    except TypeError:
        return render(request,'network/profile.html',{
        'username':who.username,
        'user_id':who.id,
        'following':who.follower.count(),
        'follower':who.following.count(),
        'button': 'Follow',
        'posts': posts,
        'lookingatown': who.username==request.user.username,
        'page_obj': page_obj
    })

    userfollowing=Follow.objects.get(user=request.user)
    whofollower=Followers.objects.get(user=who)
    
    if request.method=='POST':
        if who in userfollowing.following.all():
            
            userfollowing.following.remove(who)
            whofollower.follower.remove(request.user)

        else:
            userfollowing.following.add(who)
            whofollower.follower.add(request.user)

    if who in userfollowing.following.all():
        return render(request,'network/profile.html',{
            'username':who.username,
            'user_id':who.id,
            'following':who.follower.count(),
            'button': 'Unfollow',
            'posts': posts,
            'follower':who.following.count(),
            'page_obj': page_obj,
            'lookingatown': who.username==request.user.username

        })
    else:
        return render(request,'network/profile.html',{
            'username':who.username,
            'user_id':who.id,
            'following':who.follower.count(),
            'follower':who.following.count(),
            'posts': posts,
            'button': 'Follow',
            'page_obj': page_obj,
            'lookingatown': who.username==request.user.username
        })
            

def followingapi(request):
    try:
            following=Follow.objects.get(user=request.user)
    except Follow.DoesNotExist:
            following=request.user.following.create(user=request.user)
            following.following.remove(request.user)
    userfollowed=following.following.all()
    posts=[]
    postserailized=[]
    for i in userfollowed:
        post=Post.objects.filter(user=i)
        posts.append(post)
    for i in posts:
        new=addlikebyuser(request,i)
        postserailized+=new
    return JsonResponse(postserailized,safe=False)



def followingpage(request):
    try:
            following=Follow.objects.get(user=request.user)
    except Follow.DoesNotExist:
            following=request.user.following.create(user=request.user)
            following.following.remove(request.user)
    userfollowed=following.following.all()
    posts=Post.objects.filter(user__in=userfollowed)
    posts = posts.order_by("-timestamp").all()
    paginator=Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'network/following.html',{
        'posts':posts,
        'page_obj': page_obj,
    })
