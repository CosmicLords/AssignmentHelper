from csv import excel_tab
import email
from multiprocessing import context
import profile
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.
from .models import Notification, Topic, Notes, Profile
from .forms import NotificationForm, NotesForm, ProfileForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


#-----------------------Sign Up And Login------------------------------------

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
    form1 = UserCreationForm()
    form2 = ProfileForm()
    if request.method == 'POST':
        form1 = UserCreationForm(request.POST)
        form2 = ProfileForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit = False)
            user.save()
            profile = form2.save(commit = False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
    context = {'form1' : form1, 'form2' : form2}
    return render(request, 'base/sign_up.html' ,context)

def logoutUser(request):
    logout(request)
    return redirect('login')


#---------------------end of Sign Up Login----------------------------------



#-------------------------Home Page-------------------------------------------

def home(request):
    user_profile = Profile.objects.get(user = request.user)
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
    context = {'notifications' : notifications, 'topics' : topics, 'number_notifications' : number_notifications, 'page' : 'home', 'user_profile' : user_profile}
    return render(request, 'base/home.html', context)


#-------------End HomePage-----------------------------------


#------------------------------------Profile-------------------------

def userProfile(request, pk):
    user_profile = Profile.objects.get(user = request.user)
    user = User.objects.get(id = pk)
    profile = Profile.objects.get(user = user)
    notifications = Notification.objects.filter(host = user)
    context = {'user' : user, 'notifications' : notifications, 'profile' : profile, 'user_profile' : user_profile}
    return render(request, 'base/profile.html', context)

def changePass(request, pk):
    user_profile = Profile.objects.get(user = request.user)
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
    context = {'form' : form, 'user_profile' : user_profile}
    return render(request, 'base/change_pass.html', context)




def makeNewCR(request):
    user_profile = Profile.objects.get(user = request.user)
    context = {'user_profile' : user_profile}
    if request.method == 'POST':
        try:
            id = request.POST.get('id')
            user = User.objects.get(id = id)
            if not user is None:
                user.is_superuser = True
                user.is_staff = True
                user.save()
                return redirect('home')
            else:
                messages.error(request, 'Wrong User Id')
        except:
            messages.error(request, 'Wrong User Id')
    return render(request, 'base/new_cr_form.html', context)



def updateProfile(request, pk):
    user = User.objects.get(id = pk)
    profile = Profile.objects.get(user = user)
    form = ProfileForm(instance = profile)
    if request.method == 'POST':
        profile.description = request.POST.get('description')
        profile.PRN = request.POST.get('PRN')
        profile.name = request.POST.get('name')
        profile.save()
        return redirect('home')
    context = {'form' : form}
    return render(request, 'base/profile_update.html' ,context)

#--------------------------------End Profile------------------------------



#-------------------------------Notification----------------------------------

def notification(request, pk):
    user_profile = Profile.objects.get(user = request.user)
    notification = Notification.objects.get(id = pk)
    context = {'notification': notification, 'user_profile' : user_profile}
    return render(request, 'base/notification.html', context)


def createNotification(request):
    user_profile = Profile.objects.get(user = request.user)
    form = NotificationForm()
    context = {'form' : form, 'user_profile' : user_profile}
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
    user_profile = Profile.objects.get(user = request.user)
    notification = Notification.objects.get(id = pk)
    form = NotificationForm(instance = notification)


    context = {'form' : form, 'user_profile' : user_profile}
    
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance = notification)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/notification_form.html', context)


def deleteNotification(request, pk):
    user_profile = Profile.objects.get(user = request.user)
    notification = Notification.objects.get(id = pk)
    context = {'obj' : notification, 'user_profile' : user_profile}
    if request.method == 'POST':
        notification.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)




#--------------------------------End Notification-----------------------------





#------------------------------------Notes------------------------------
def notesPage(request):
    user_profile = Profile.objects.get(user = request.user)
    notes = Notes.objects.all()
    number_notes = notes.count()
    topics = Topic.objects.all()
    context = {'notes' : notes, 'topics' : topics, 'number_notes' : number_notes, 'page' : 'notes', 'user_profile' : user_profile}
    return render(request, 'base/notes.html', context)


def addNotes(request):
    user_profile = Profile.objects.get(user = request.user)
    form = NotesForm
    context = {'form' : form, 'page' : 'notes', 'user_profile' : user_profile}
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = form.save(commit = False)
            notes.host = request.user
            notes.save()
        return redirect('notes')
    return render(request, 'base/notes_form.html', context)



#--------------------------------End Notes-------------------------




