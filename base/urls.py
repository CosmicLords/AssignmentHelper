from django.urls import path
from . import views

urlpatterns = [
    # ---------------------------------------------------------------------------
    path('', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('signup/', views.signUp, name = "sign-up"),
    #-----------------------------------------------------------------------------
    path('home/', views.home, name = "home"),
    path('notes/', views.notesPage, name = "notes"),
    #-----------------------------------------------------------------------------
    path('notification/<str:pk>/', views.notification, name = "notification"),
    path('create-notification/', views.createNotification, name = "create-notification"),
    path('update-notification/<str:pk>/', views.updateNotification, name = "update-notification"),
    path('delete-notification/<str:pk>/', views.deleteNotification, name = "delete-notification"),
    #-----------------------------------------------------------------------------
    path('profile/<str:pk>/', views.userProfile, name = "user-profile"),
    path('profile/<str:pk>/change-pass', views.changePass, name = "change-password"),
    path('profile/<str:pk>/update', views.updateProfile, name = "update-profile"),
    
    path('create-new-cr/', views.makeNewCR, name = "make-new-cr"),
    path('add-notes/', views.addNotes, name = "add-notes"),
]