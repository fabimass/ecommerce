from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=64, default="Other")
    image = models.URLField(blank=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_owned")
    is_active = models.BooleanField(default=True)
    users_watching = models.ManyToManyField(User, blank=True, related_name="listings_watched")
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"${self.bid} - {self.bidded_by}"

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.item}: {self.comment}"