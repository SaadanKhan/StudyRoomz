#-------------------Sample For every Project
from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRoutes),
#------------------- For every Project
    path('rooms/',views.getRooms),
    path('rooms/<str:pk>/',views.getRoom),
]