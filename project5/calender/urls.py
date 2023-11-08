from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('<int:year>/<int:month>',views.othermonth,name='othermonth'),
    path('weekview',views.weekview,name='weekview'),
    path('editevent',views.editevent,name='editevent'),

    #API
    path('events/<int:year>/<int:month>',views.eventapi,name='eventapi'),
    path('weekevent',views.weekeventapi,name='weekevent')
]