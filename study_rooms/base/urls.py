from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="base.login"),
    path('logout/', views.logoutUser, name="base.logout"),
    path('register/', views.registerPage, name="base.register"),
    path("home/", views.home, name="base.home"),
    path("room/<str:pk>/", views.room, name="base.room"),
    path("profile/<str:pk>", views.userProfile, name="base.userProfile"),
    path("create-room/", views.createRoom, name="base.createRoom"),
    path("update-room/<str:pk>/", views.updateRoom, name="base.updateRoom"),
    path("delete-room/<str:pk>", views.deleteRoom, name="base.deleteRoom"),
    path("delete-message/<str:pk>", views.deleteMessage, name="base.deleteMessage"),
]