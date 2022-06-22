from django.contrib import admin

# Register your models here.

from .models import  Notification, Topic, Comment, Notes, Profile

admin.site.register(Notification)
admin.site.register(Comment)
admin.site.register(Topic)
admin.site.register(Notes)
admin.site.register(Profile)