from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


def index(request):
    listings = Listing.objects.filter(open=True).order_by('-date_added')
    return render(request, "auctions/index.html", {
        "listings": listings
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new(request):
    if request.method == 'POST':
        form = NewListing(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.open = True
            new.save()
            return HttpResponseRedirect("/")
    return render(request, "auctions/new.html", {
        "form": NewListing()
        })

def listing(request, listingid):
    ownbid = False
    ownlisting = False
    winning_bid = 0
    user = request.user

    # Get listing
    listing = get_object_or_404(Listing, pk=listingid)

    # Check if watching
    watching = False
    if user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user)
        for i in watchlist:
            if listingid == i.listing_id:
                watching = True

    # Access model for latest bid
    latestbid = Bid.objects.filter(listing=listingid).order_by("-amount").first()

    # Display latest bid or starting bid
    lastbid = latestbid
    if lastbid == None:
        bid = float(listing.price)
        lastbid = float("{:.2f}".format(bid))
    else:
        lastbid = lastbid.amount

    try:
        comments = Comment.objects.filter(listing=listingid).order_by('-datetime')
    except:
        comments = None

    if user.is_authenticated:
        try: 
            ownlisting = bool(listing.user_id == user.id)
        except:
            ownlisting = False

        # Find out if there was a last bid and if belongs to current user
        try:
            ownbid = bool(latestbid.user_id == user.id)
        except:
            ownbid = False
    
        # Save new bid
        if request.method == 'POST':
            if "bid" in request.POST:
                form = PlaceBid(request.POST, instance=latestbid)
                if form.is_valid():
                    bid = form.save(commit=False)
                    if float(bid.amount) <= lastbid:
                        return render(request, "auctions/listing.html", {
                        "listing": listing, "message": "Bid must be higher than current bid."
                    })
                    bid.user = request.user
                    bid.listing = listing
                    listing.price = bid.amount
                    bid.save()
                    listing.save()
                    return HttpResponseRedirect(listing.get_absolute_url())
                else:
                    print(form.errors)

    # Get winning bid for closed listings
    if not listing.open:
        winning_bid = get_winner(listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": PlaceBid(),
        "lastbid": lastbid,
        "watching": watching,
        "loggedin": request.user.is_authenticated,
        "bids": Bid.objects.filter(listing=listingid).count(),
        "ownbid": ownbid,
        "ownlisting": ownlisting,
        "winner": winning_bid,
        "comments": comments,
        "commentform": NewComment(),
        })

def closebid(request, listingid):
    listing = Listing.objects.get(pk=listingid)
    listing.open = False
    listing.save()
    return redirect('listing',listingid=listingid)

@login_required
def addwatchlist(request, listingid):
    wl = Watchlist.objects.filter(listing=listingid)
    if not wl:
        watch = Watchlist()
        watch.listing = Listing.objects.get(id=listingid)
        watch.user = User.objects.get(id=request.user.id)
        watch.save()
    elif wl:
        wl.delete()
    return redirect(watchlist)


@login_required
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user.id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
        })

def get_winner(listingid):
    winning_bid = Bid.objects.filter(listing=listingid).order_by("-amount").first()
    return winning_bid

def addcomment(request, listingid):
    if request.method == 'POST':
        commentform = NewComment(request.POST)
        if commentform.is_valid():
            c = commentform.save(commit=False)
            c.comment = commentform.cleaned_data['comment']
            c.user = request.user
            c.listing = Listing.objects.get(id=listingid)
            c.save()
            return redirect('listing',listingid=listingid)

def categorypage(request, categoryid):
    listings = Listing.objects.filter(category=categoryid, open=True)
    category = None
    for listing in listings:
        category = listing.get_category_display()
    return render(request, "auctions/category.html", {
        "category": category, "listings": listings
    })