from django.contrib import admin
from .models import Listing, Bid, Comment, User

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "category", "listed_by", "is_active")
    filter_horizontal = ("users_watching",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("item", "bid", "bidded_by", "date")

# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(User)