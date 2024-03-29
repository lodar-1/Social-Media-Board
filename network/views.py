import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .models import User, Post
from django.http import JsonResponse
from .db import *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages

itemsPerPage = 10

def index(request, pagecount=1):
	try: 
		if "following" in request.path:
			return render(request, "network/index.html", {"following": True})
		else:
			return render(request, "network/index.html", {"following": False})
	except Exception as e:
		messages.error(request, f"An error occured, {e}, please try again")
		return render(request, "network/index.html", {"following": False})

def posts(request, userby = None, page = 1):
	try: 
		if userby:
			posts = returnPosts(request.user.id, userby)
		else:
			posts = returnPosts(request.user.id)
		# ~ APPEND CURRENT USERID TO DICT
		for post in posts:
			post['currentuser'] = request.user.id
		paginator = Paginator(posts, itemsPerPage)
		page = paginator.get_page(page)
		pagecount = paginator.num_pages
		page.object_list[0]["pagecount"] = pagecount	
		return JsonResponse(page.object_list, safe=False)
	except Exception as e:
		messages.error(request, f"An error occured, {e}, please try again")
		return render(request, "network/index.html", {"following": False})
def login_view(request):
	try:
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
	except Exception as e:
		messages.error(request, f"An error occured, {e}, please try again")
		return render(request, "network/index.html", {"following": False})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
	try:
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
	except Exception as e:
		messages.error(request, f"An error occured, {e}, please try again")
		return render(request, "network/index.html", {"following": False})
		
@login_required(login_url="/login")
@csrf_exempt
def newpost(request):
	try:
		data = json.loads(request.body)
		if request.method == "POST":
			newpost = Post.objects.create(user = request.user, post_date=datetime.now(), content=data.get("content"))
			return HttpResponseRedirect(reverse("index"))
		elif request.method == "PUT":
			post = Post.objects.get(id=data.get("postid"))
			post.content = 	data.get("content")
			post.save()
			return HttpResponseRedirect(reverse("index"))
	except Exception as e:
		messages.error(request, f"An error occured, {e}, please try again")
		return render(request, "network/index.html", {"following": False})
		
@csrf_exempt
def follow(request):
	try: 
		data = json.loads(request.body)
		toggleFollow(request.user.id, data.get("follow"), data.get("followadd"))
		return profile(request, data.get("followuser"))
	except Exception as e:
		messages.error(request, f"An error occured, {e}, please try again")
		return render(request, "network/index.html", {"following": False})

@csrf_exempt		
def like(request):
	try:
		data = json.loads(request.body)
		result = toggleLike(request.user.id, data.get("postid"), data.get("like"))
		return JsonResponse(result, safe=False)
	except Exception as e:
		messages.error(request, f"An error occured, {e}, please try again")
		return render(request, "network/index.html", {"following": False})
		
def post(request, postid):
	try: 
		post1 = returnPost(postid)
		return JsonResponse(post1, safe=False)	
	except Exception as e:
		messages.error(request, f"An error occured, {e}, please try again")
		return render(request, "network/index.html", {"following": False})	

@login_required(login_url="/login")	
def profile(request, userid):
	try:
		follows = returnFollow(int(userid))
		isfollowing = returnIsFollowing(request.user.id, int(userid))
		return render(request, "network/profile.html", {
					"user": follows.get("username"), "followers": follows.get("following"), "followed": follows.get("followed"), 
					"userid": int(userid), "currentuser": request.user.id, "isfollowing": isfollowing, "following": True
				})
	except Exception as e:
		messages.error(request, f"An error occured, {e}, please try again")
		return render(request, "network/index.html", {"following": False})
					
def following(request):
	return index(request)
	
def loadfollowing(request, page=1):
	try:
		posts = returnPosts(request.user.id, following=True)
		for post in posts:
			post['currentuser'] = request.user.id
		paginator = Paginator(posts, itemsPerPage)
		page = paginator.get_page(page)	
		pagecount = paginator.num_pages
		page.object_list[0]["pagecount"] = pagecount
		return JsonResponse(page.object_list, safe=False)
	except Exception as e:
		messages.error(request, f"An error occured, {e}, please try again")
		return render(request, "network/index.html", {"following": False})	
		
			
