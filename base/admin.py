from django.contrib import admin

# Register your models here.

from .models import  Notification, Topic, Notes, Profile

admin.site.register(Notification)
admin.site.register(Topic)
admin.site.register(Notes)
admin.site.register(Profile)