from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    item = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id}: {self.name} (${self.price})"

class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.item}: ${self.bid}"

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.item}: {self.comment}"