from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Event(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE,related_name='events')
    eventname=models.CharField(max_length=255)
    description=models.TextField()
    when=models.DateTimeField()
    till=models.DateTimeField()

    def serailize(self):
        return {
            "user": self.user.username,
            "eventname": self.eventname,
            "when": self.when.strftime("%b %d %Y, %H:%M"),
            "till": self.till.strftime("%b %d %Y, %H:%M"),
            "description":self.description,
            'day':str(int(self.when.strftime('%d')))+str(int(self.when.strftime('%m')))+self.when.strftime('%Y'),
            'whenhour':str(int(self.when.strftime('%d')))+str(int(self.when.strftime('%m')))+self.when.strftime('%H')+self.when.strftime('%M'),
            'tillhour':str(int(self.till.strftime('%d')))+str(int(self.till.strftime('%m')))+self.till.strftime('%H')+self.till.strftime('%M')
        }
    
    def whenhourandmin(self):
        return self.when.strftime('%H%M')

    def tillhourandmin(self):
        return self.till.strftime('%H%M')