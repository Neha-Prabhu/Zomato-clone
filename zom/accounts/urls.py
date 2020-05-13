from django.urls import path
from . import views
urlpatterns =[
   path('newregistration',views.newreg,name='newregistration'),
   path('login',views.login,name='login'),
   path('logout',views.logout,name='logout')
]