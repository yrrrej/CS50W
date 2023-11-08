from django.contrib import admin
from network.models import Like,Post,Follow,Followers,User
# Register your models here.

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Followers)
admin.site.register(User)