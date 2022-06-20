from django.contrib import admin

# Register your models here.

from .models import  Notification, Topic, Comment

admin.site.register(Notification)
admin.site.register(Comment)
admin.site.register(Topic)