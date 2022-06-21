from dataclasses import fields
from django.forms import ModelForm
from .models import Notification, User

class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
        exclude = ['host']
