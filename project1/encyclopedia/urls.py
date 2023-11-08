from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>/', views.entry, name='entry'),
    path('search_result',views.search ,name='search'),
    path('error',views.error,name='error'),
    path('create',views.create,name='create'),
    path('edit/<str:title>/',views.edit , name='edit'),
    path('random',views.randompage,name='random')
]
