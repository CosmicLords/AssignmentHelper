from django.forms import ModelForm
from .models import Notification

class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
        exclude = ['host']

