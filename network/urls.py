
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("new", views.newpost, name="new"),
	path("like", views.like, name="like"),
	path("follow", views.follow, name="follow"),
	path("posts/<int:postid>", views.post, name="post"),
	path("profile/<str:userid>", views.profile, name="profile"),
	path("<int:userby>", views.posts, name="profile"),
	path("following", views.following, name="following"),
	path("loadfollowing", views.loadfollowing, name="loadfollowing"),

]

