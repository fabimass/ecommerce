from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=64, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_owned")
    date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    users_watching = models.ManyToManyField(User, blank=True, related_name="listings_watched")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions_won", blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    def current_bid(self):
        bids_list = Bid.objects.filter(item=self).order_by('-date')
        if len(bids_list) > 0 :
            return bids_list[0]
        else:
            return None 

    def bids_count(self):
        return len(Bid.objects.filter(item=self))

class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    date = models.DateTimeField()

    def __str__(self):
        return f"${self.bid} - {self.bidded_by} on {self.item}"

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.comment} - {self.commented_by} on {self.item}"