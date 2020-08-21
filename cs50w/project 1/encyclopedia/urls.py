from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_page, name="random"),
    path("create", views.create, name="create"),
    path("wiki/<str:article>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("search", views.search, name="search"),
]
