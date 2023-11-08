from django.contrib import admin

from auctions.models import Listing, Comment,User,Bid,Watchlist,ClosedListing
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display=('id','title','description','starting_bid','listed_by')

class BidAdmin(admin.ModelAdmin):
    list_display=('id','bid','bid_by','bid_on')

class CommentAdmin(admin.ModelAdmin):
    list_display=('comment','comment_by','comment_on')

admin.site.register(Listing,ListingAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(ClosedListing)
