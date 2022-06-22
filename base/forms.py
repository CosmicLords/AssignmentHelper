from dataclasses import field, fields
from pyexpat import model
from django.forms import ModelForm
from .models import Notification, User, Notes, Profile

class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
        exclude = ['host']

class NotesForm(ModelForm):
    class Meta:
        model = Notes
        fields = '__all__'
        exclude = ['host']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
