import debug_toolbar
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from .views import HomeView,NewVideo,CommentView,LoginView,SignUpView,LogoutView,VideoView
app_name= 'youtube'
urlpatterns = [
    path('', HomeView.as_view(),name='home'),
    path('new_video/',NewVideo.as_view(),name='newVid'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/',SignUpView.as_view(),name='register'),  
    path('comment',CommentView.as_view(),name='comment'),
    path('video/<int:id>',VideoView.as_view(),name='video'), 
 
]

