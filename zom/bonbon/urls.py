from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static
  

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("regform.html", views.register, name="registerdets"),
    path("homepage", views.rwelcome, name="rwelcome"),
    path("frate", views.sortprice, name="sotrprice"),
    path("fprice", views.sortrate, name="sortrate"),
    path("homepage.html", views.welcome, name="welcome"),
    path("searchres", views.searchres, name="searchres"),
    path("subbill", views.subbill, name="subbill"),
    path("storevisits", views.storevisits, name="storevisits"),
    path('newregistration',views.newreg,name='newregistration'),
    path('lunch',views.lunch,name='lunch'),
    path('dinner',views.dinner,name='dinner'),
    path('breakfast',views.breakfast,name='breakfast'),
    path('nlife',views.nightlife,name='nlife'),
    path('cafe',views.cafe,name='cafe'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('chart',views.chart,name='chart')
]


