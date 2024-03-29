
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('profile/<str:username>',views.profile,name='profile'),
    path('following',views.followingpage,name='following'),
    #API route
    path('followingapi',views.followingapi,name='followingapi'),
    path('profileapi/<int:user_id>',views.profileAPI,name='profileAPI'),
    path('posts',views.posts,name='posts'),
    path('likes/<int:post_id>',views.likes,name='likes')
]
