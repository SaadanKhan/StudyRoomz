from django.urls import path
from . import views


urlpatterns = [
    path('index', views.index, name='home'),
    path('room/<str:pk>/',views.room, name='room'),
    path('create-room/',views.CreateRoom, name='create-room'),
    path('update-room/<str:pk>/',views.UpdateRoom, name='update-room'),
    path('delete-room/<str:pk>/',views.Delete, name='delete-room'),
    path('delete-message/<str:pk>/',views.DeleteMessage, name='delete-message'),
    path('profile/<str:pk>/',views.UserProfile, name='user-profile'),
    path('login/',views.loginPage, name='login-page'),
    path('logout/',views.LogoutPage, name='logout'),
    path('signup/',views.Signup, name='signup'),
    path('update-user/',views.UpdateUser, name='update-user'),
]

