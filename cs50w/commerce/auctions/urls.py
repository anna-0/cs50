from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("listing/<int:listingid>/", views.listing, name="listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("addwatchlist/<int:listingid>/", views.addwatchlist, name="addwatchlist"),
    path("closebid/<int:listingid>/", views.closebid, name="closebid"),
    path("addcomment/<int:listingid>/", views.addcomment, name="addcomment"),
    path("category/<str:categoryid>/", views.categorypage, name="categorypage"),
]
