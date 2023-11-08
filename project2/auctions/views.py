from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import Listing,Comment,Bid,Watchlist,ClosedListing
from django.db.models import Avg, Max, Min, Sum
from .models import User


def index(request):
    return render(request, "auctions/index.html",{
        'listings':Listing.objects.filter(closed__isnull=True)
        
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


def listing(request,listing_id):
    listing=Listing.objects.get(pk=listing_id)
    currentbid=listing.currentbid()
    try: #check if listing is closed and if it is not closed, continue
        Listing.objects.get(closed__isnull=True,pk=listing_id)
    
    except Listing.DoesNotExist: #If listing is closed

        if listing.currentbid()!=listing.starting_bid: #If there are biddings
            winning_bid=Bid.objects.get(bid_on_id=listing_id,bid=currentbid)
            if request.user==winning_bid.bid_by: #If there are biddings, only winner can see that they have won
                return render(request,'auctions/listing.html',{
                            'closed':'Listing is closed, you have won the auction.'
                            })
            else:
                return render(request,'auctions/listing.html',{
                            'closed':'Listing is closed.'
                            })
        elif listing.currentbid()==listing.starting_bid: #If the bid is the same as the starting bid
            try: #check if there are bidders
                winning_bid=Bid.objects.get(bid_on_id=listing_id,bid=currentbid)
            except Bid.DoesNotExist: #If no bidders
                return render(request,'auctions/listing.html',{
                            'closed':'Listing is closed.'
                            })
            if request.user==winning_bid.bid_by: # If request.user is bidder
                return render(request,'auctions/listing.html',{
                            'closed':'Listing is closed, you have won the auction.'
                            })
            else: # Everyone else
                return render(request,'auctions/listing.html',{
                            'closed':'Listing is closed.'
                            })
        else: #Not winner
            return render(request,'auctions/listing.html',{
                            'closed':'Listing is closed.'
                            })
    
    if listing.currentbid()!=listing.starting_bid: # there there are biddings

        if 'Comment' in request.POST and request.method=="POST": #comment request there are biddings
            new_comment=request.POST['new_comment']
            if new_comment is not None:
                new=Comment.objects.create(comment=new_comment,comment_by=request.user,comment_on=listing)
                return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'bids':Bid.objects.get(bid_on_id=listing_id,bid=currentbid),
                })

        elif 'Bid' in request.POST and request.method=="POST": #bid request there are biddings
            new_bid=request.POST['new_bid']
            if currentbid>=int(new_bid):
                return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'bids':Bid.objects.get(bid_on_id=listing_id,bid=currentbid),
                "message": "Bid must be greater than current bid.",
                })
            else:
                if new_bid is not None:
                    new=Bid.objects.create(bid=new_bid,bid_by=request.user,bid_on=listing)
                    currentbid=listing.currentbid()
                    return render(request,'auctions/listing.html',{
                    'listing':listing,
                    'comments':Comment.objects.filter(comment_on_id=listing_id),
                    'bids':Bid.objects.get(bid_on_id=listing_id,bid=currentbid),
                    })     

        elif 'Close' in request.POST and request.method=='POST': #close request there are biddings
            if request.user==listing.listed_by:
                close=ClosedListing.objects.get(pk=1)
                Listing.objects.filter(pk=listing_id).update(closed=close)
                return render(request,'auctions/listing.html',{
                        'listing':Listing.objects.get(closed__isnull=False,pk=listing_id),
                        'comments':Comment.objects.filter(comment_on_id=listing_id),
                        'bids':Bid.objects.get(bid_on_id=listing_id,bid=currentbid),
                        'closed':'Auction is closed'
                        })
            else:
                return render(request,'auctions/listing.html',{
                        'listing':Listing.objects.get(pk=listing_id),
                        'comments':Comment.objects.filter(comment_on_id=listing_id),
                        'bids':Bid.objects.get(bid_on_id=listing_id,bid=currentbid),
                        'noauthoritytoclose':'You have no authority to close this listing'
                        })

        elif 'Watchlist' in request.POST and request.method=='POST': #Watchlist request and there are biddings
            try: #Checks if user have an existing watchlist
                new=Watchlist.objects.get(user_watchlist=request.user)
            except Watchlist.DoesNotExist: #If not create watchlist and add listing for user 
                new_watchlist=listing.watchlist.create(user_watchlist=request.user)
                return render(request,'auctions/listing.html',{
                    'listing':listing,
                    'comments':Comment.objects.filter(comment_on_id=listing_id),
                    'starting_bid':listing.starting_bid,
                    'bids':Bid.objects.get(bid_on_id=listing_id,bid=currentbid),
                    'listingadded': 'Listing have been added into your watchlist'
                    }) 
            new.watchlist.add(listing)
            return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'starting_bid':listing.starting_bid,
                'bids':Bid.objects.get(bid_on_id=listing_id,bid=currentbid),
                'listingadded': 'Listing have been added into your watchlist'
                }) 

        elif 'RemoveWatchlist' in request.POST and request.method=='POST': #Remove listing from watchlist and there are biddings
            try:#Checks if user have watchlist
                user=Watchlist.objects.get(user_watchlist=request.user)
            except Watchlist.DoesNotExist:
                return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'starting_bid':listing.starting_bid,
                'bids':Bid.objects.get(bid_on_id=listing_id,bid=currentbid),
                'listingremoved': 'Listing have been removed into your watchlist'
                }) 
            listing.watchlist.remove(user)
            return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'starting_bid':listing.starting_bid,
                'bids':Bid.objects.get(bid_on_id=listing_id,bid=currentbid),
                'listingremoved': 'Listing have been removed into your watchlist'
                }) 

        else:#no request and there are biddings
            return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'starting_bid':listing.starting_bid,
                'bids':Bid.objects.get(bid_on_id=listing_id,bid=currentbid),
                })         
    
    else: #if there is no bids

        if 'Comment' in request.POST and request.method=="POST":  #comment request and no bids
            new_comment=request.POST['new_comment']
            if new_comment is not None:
                new=Comment.objects.create(comment=new_comment,comment_by=request.user,comment_on=listing)
                return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'starting_bid':listing.starting_bid
                })

        elif 'Bid' in request.POST and request.method=="POST":   #bids request and no bids
            new_bid=request.POST['new_bid']
            if currentbid>int(new_bid):
                return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'starting_bid':listing.starting_bid,
                "message": "Bid must be greater than current bid.",
                })
            else:
                if new_bid is not None:
                    new=Bid.objects.create(bid=new_bid,bid_by=request.user,bid_on=listing)
                    currentbid=listing.currentbid()
                    return render(request,'auctions/listing.html',{
                    'listing':listing,
                    'comments':Comment.objects.filter(comment_on_id=listing_id),
                    'bids':Bid.objects.get(bid_on_id=listing_id,bid=currentbid),
                    })      

        elif 'Close' in request.POST and request.method=='POST': #close request and no bids
            if request.user==listing.listed_by:
                close=ClosedListing.objects.get(pk=1)
                Listing.objects.filter(pk=listing_id).update(closed=close)
                return render(request,'auctions/listing.html',{
                        'listing':Listing.objects.get(closed__isnull=False,pk=listing_id),
                        'comments':Comment.objects.filter(comment_on_id=listing_id),
                        'starting_bid':listing.starting_bid,
                        'closed':'Auction is closed'
                        })
            else:
                return render(request,'auctions/listing.html',{
                        'listing':Listing.objects.get(pk=listing_id),
                        'comments':Comment.objects.filter(comment_on_id=listing_id),
                        'starting_bid':listing.starting_bid,
                        'noauthoritytoclose':'You have no authority to close this listing'
                        })
                        
        elif 'Watchlist' in request.POST and request.method=='POST': #Watchlist request and no bids
            try:
                new=Watchlist.objects.get(user_watchlist=request.user)
            except Watchlist.DoesNotExist:
                new_watchlist=listing.watchlist.create(user_watchlist=request.user)
                return render(request,'auctions/listing.html',{
                    'listing':listing,
                    'comments':Comment.objects.filter(comment_on_id=listing_id),
                    'starting_bid':listing.starting_bid,
                    'listingadded': 'Listing have been added into your watchlist'
                    }) 
            new.watchlist.add(listing)
            return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'starting_bid':listing.starting_bid,
                'listingadded': 'Listing have been added into your watchlist'
                }) 

        elif 'RemoveWatchlist' in request.POST and request.method=='POST': #Remove listing from watchlist and no bids
            try:#Checks if user have watchlist
                user=Watchlist.objects.get(user_watchlist=request.user)
            except Watchlist.DoesNotExist:
                return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'starting_bid':listing.starting_bid,
                'listingremoved': 'Listing have been removed into your watchlist'
                }) 
            listing.watchlist.remove(user)
            return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'starting_bid':listing.starting_bid,
                'listingremoved': 'Listing have been removed into your watchlist'
                })

        else: #no request and no bids
            return render(request,'auctions/listing.html',{
                'listing':listing,
                'comments':Comment.objects.filter(comment_on_id=listing_id),
                'starting_bid':listing.starting_bid
            }) 

def create(request):
    if request.method=='POST':
        t=request.POST['t']
        d=request.POST['d']
        c=request.POST['c']
        img_url=request.POST['img_url']
        starting_bid=request.POST['starting_bid']
        if t and starting_bid is not None:
            new=Listing.objects.create(title=t,description=d,img_url=img_url,starting_bid=starting_bid,listed_by=request.user,category=c)
            new.save()
            return HttpResponseRedirect(reverse('listing',args=(new.id,)))
    else:
        return render(request,'auctions/create.html')


def watchlist(request):
    try:
        user_watchlist=Watchlist.objects.get(user_watchlist=request.user)
    except Watchlist.DoesNotExist:
        return render(request,'auctions/watchlist.html',{
        'nowatchlist':'You do not have any listing on your watchlist'
    })
    return render(request,'auctions/watchlist.html',{
        'watchlist':user_watchlist.watchlist.all()
    })

def category(request):
    listings=Listing.objects.all()
    all_category={x.category for x in listings if x.category!=''}
    

    return render(request,'auctions/category.html',{
        'categories':all_category
        })

def whichcategory(request,categoryname):
    listings=Listing.objects.filter(category=categoryname,closed__isnull=True)
    return render(request,'auctions/index.html',{
        'listings':listings
    })
