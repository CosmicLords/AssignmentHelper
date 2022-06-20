from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('adduser/', views.addUser, name = "add-user"),
    path('', views.home, name = "home"),
    path('notification/<str:pk>/', views.notification, name = "notification"),
    path('profile/<str:pk>/', views.userProfile, name = "user-profile"),
    path('create-notification/', views.createNotification, name = "create-notification"),
    path('update-notification/<str:pk>/', views.updateNotification, name = "update-notification"),
    path('delete-notification/<str:pk>/', views.deleteNotification, name = "delete-notification"),
]