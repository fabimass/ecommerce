from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing
from .forms import ListingForm


def index(request):
    listings = Listing.objects.filter(is_active=True)
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
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = Listing(
                title=form.cleaned_data["title"], 
                price=form.cleaned_data["price"], 
                category=form.cleaned_data["category"],
                description=form.cleaned_data["description"],
                image=form.cleaned_data["image"],
                listed_by=request.user)
            listing.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/new.html", {
            "form": ListingForm()
        })


def listing(request, id):
    try:
        listing = Listing.objects.get(pk=id)
        return render(request, "auctions/listing.html", {
            "listing": listing
        })
    except:
        return render(request, "auctions/404.html")


def watchlist(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def watch(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        listing.users_watching.add(request.user)

    return HttpResponseRedirect(reverse("watchlist"))