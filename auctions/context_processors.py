
def watchlist_context_processor(request):
    if request.user.is_authenticated:
        watchlist_count = len(request.user.listings_watched.all())
    else:
        watchlist_count = 0
    return {
        "watchlist_count": watchlist_count
    }