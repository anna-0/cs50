
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # API routes
    path("add-post", views.add_post, name="add-post"),
    path("post/<int:post_id>", views.post, name="post"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow"),
    path("user/<username>", views.profile, name="profile"),
    path("user/<str:username>/following", views.following, name="following"),
]   
