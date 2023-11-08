from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg, Max, Min, Sum

class User(AbstractUser):
    pass

class ClosedListing(models.Model):
    closed_id=models.IntegerField(blank=True,null=True)

class Listing(models.Model):
    title=models.CharField(max_length=64)
    description=models.CharField(max_length=64,blank=True,null=True)
    starting_bid=models.IntegerField()
    img_url=models.URLField(blank=True,null=True)
    listed_by=models.ForeignKey(User,blank=False,on_delete=models.CASCADE,)
    closed=models.ForeignKey(ClosedListing,on_delete=models.CASCADE,blank=True,null=True)
    category=models.CharField(max_length=64,blank=True)

    def currentbid(self):
        if self.bids.all().aggregate(Max('bid'))['bid__max']==None:
            return self.starting_bid
        else:
            return self.bids.all().aggregate(Max('bid'))['bid__max']
    


class Comment(models.Model):
    comment=models.CharField(max_length=64)
    comment_by=models.ForeignKey(User,blank=False,on_delete=models.CASCADE,)
    comment_on=models.ForeignKey(Listing,blank=True,on_delete=models.CASCADE,related_name='comments')

    def __str__(self):
        return f'{self.comment}'

class Bid(models.Model):
    bid=models.IntegerField()
    bid_by=models.ForeignKey(User,blank=False,on_delete=models.CASCADE,null=True)
    bid_on=models.ForeignKey(Listing,blank=True,on_delete=models.CASCADE,related_name='bids',)

    def __str__(self):
        return f'{self.bid}'

    def __int__(self):
        return int(f'{self.bid}')
    

class Watchlist(models.Model):
    watchlist=models.ManyToManyField(Listing,blank=True,related_name='watchlist')
    user_watchlist=models.ForeignKey(User,blank=True,on_delete=models.CASCADE)

