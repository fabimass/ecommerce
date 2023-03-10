from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, Listing, Bid, Comment
from .forms import ListingForm, BidForm, MessageForm


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": "Active Listings"
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
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = Listing(
                title=form.cleaned_data["title"], 
                starting_price=form.cleaned_data["price"], 
                category=form.cleaned_data["category"] if form.cleaned_data["category"] != "" else "No category provided",
                description=form.cleaned_data["description"],
                image=form.cleaned_data["image"],
                listed_by=request.user,
                date=datetime.now())
            listing.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/new.html", {
            "form": ListingForm()
        })


def listing(request, id):
    try:
        listing = Listing.objects.get(pk=id)
        # Check if the current user has this item watchlisted
        watchlisted = listing.users_watching.filter(pk=request.user.id).exists()

        if request.method == "POST":
            form = BidForm(request.POST)
            if form.is_valid():
                price_bidded = form.cleaned_data["price"]
                bids_list = listing.bids.all()

                # The bid must be at least as large as the starting bid, 
                # and must be greater than any other bids that have been placed (if any)
                
                if ( len(bids_list) > 0 and price_bidded > bids_list[len(bids_list)-1].bid ) or ( len(bids_list) == 0 and price_bidded >= listing.starting_price ): 
                    new_bid = Bid(
                            bid=price_bidded, 
                            item=Listing.objects.get(pk=id), 
                            bidded_by=request.user,
                            date=datetime.now())
                    new_bid.save()
                    bid_status = "success"

                else:
                    bid_status = "fail"
            
            return render(request, "auctions/listing.html", {
                            "listing": listing,
                            "watchlisted": watchlisted,
                            "bid_form": BidForm(),
                            "bid_status": bid_status,
                            "comment_form": MessageForm(),
                            "comments": listing.comments.all() 
                        })
    
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "watchlisted": watchlisted,
                "bid_form": BidForm(), 
                "comment_form": MessageForm(),
                "comments": listing.comments.all() 
            })
    except:
        return render(request, "auctions/404.html")


def watchlist(request):
    current_user = request.user
    listings = current_user.listings_watched.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": f"{current_user.username}'s Watchlist"
    })


def watch(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        listing.users_watching.add(request.user)

    return HttpResponseRedirect(reverse("watchlist"))


def unwatch(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        listing.users_watching.remove(request.user)

    return HttpResponseRedirect(reverse("watchlist"))


def close(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        # Only the user who created the listing can close it
        if request.user == listing.listed_by:
            listing.is_active = False
            if listing.current_bid():
                listing.winner = listing.current_bid().bidded_by
            listing.save()

    return HttpResponseRedirect(reverse("listing", args=[id]))


def comment(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Comment(
                comment=form.cleaned_data["message"], 
                item=listing,
                commented_by=request.user,
                date=datetime.now())
            message.save()

    return HttpResponseRedirect(reverse("listing", args=[id]))


def categories(request):
    categories_list = Listing.objects.filter(is_active=True).values("category").distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories_list
    })


def category(request, category):
    listings = Listing.objects.filter(is_active=True, category=category)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": f"Category: {category}"
    })