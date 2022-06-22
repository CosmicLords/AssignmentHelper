from csv import excel_tab
import email
from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.
from .models import Notification, Topic, Notes
from .forms import NotificationForm, NotesForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong Username or Password')

    context = {}
    return render(request, 'base/login.html', context)

def signUp(request):
    form = UserCreationForm()
    context = {'form' : form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        try:
            if form.is_valid():
                user = form.save(commit = False)
                user.save()
                login(request, user)
                return redirect('home')
            
            else:
                messages.error(request, 'Something Went Wrong')
        except:
            messages.error(request, 'Something Went Wrong')

    return render(request, 'base/sign_up.html' ,context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    q = request.GET.get('q')
    if q == None:
        q = ''

    notifications = Notification.objects.filter(
        Q(topic__name__icontains = q) |
        Q(title__icontains = q) |
        Q(description__icontains = q)
    )
    number_notifications = notifications.count()
    topics = Topic.objects.all()
    context = {'notifications' : notifications, 'topics' : topics, 'number_notifications' : number_notifications, 'page' : 'home'}
    return render(request, 'base/home.html', context)

def notification(request, pk):
    notification = Notification.objects.get(id = pk)
    context = {'notification': notification}
    return render(request, 'base/notification.html', context)


def userProfile(request, pk):
    user = User.objects.get(id = pk)
    notifications = Notification.objects.filter(host = user)
    context = {'user' : user, 'notifications' : notifications}
    return render(request, 'base/profile.html', context)

def changePass(request, pk):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'base/change_pass.html', {
        'form': form
    })

def createNotification(request):
    form = NotificationForm()
    context = {'form' : form}
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            # form.save()
            notification = form.save(commit = False)
            notification.host = request.user
            notification.save()
            return redirect('home')
    return render(request, 'base/notification_form.html', context)

def updateNotification(request, pk):
    # pk -> primary key
    notification = Notification.objects.get(id = pk)
    form = NotificationForm(instance = notification)


    context = {'form' : form}
    
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance = notification)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/notification_form.html', context)


def deleteNotification(request, pk):
    notification = Notification.objects.get(id = pk)
    context = {'obj' : notification}
    if request.method == 'POST':
        notification.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)


def notesPage(request):
    notes = Notes.objects.all()
    number_notes = notes.count()
    topics = Topic.objects.all()
    context = {'notes' : notes, 'topics' : topics, 'number_notes' : number_notes, 'page' : 'notes'}
    return render(request, 'base/notes.html', context)

def makeNewCR(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = User.objects.get(id = id)
        if not user is None:
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return redirect('home')
        else:
            messages.error('Wrong User Id')

    return render(request, 'base/new_cr_form.html')


def addNotes(request):
    form = NotesForm
    context = {'form' : form, 'page' : 'notes'}
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = form.save(commit = False)
            notes.host = request.user
            notes.save()
        return redirect('notes')
    return render(request, 'base/notes_form.html', context)