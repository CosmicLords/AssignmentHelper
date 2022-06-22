from pyexpat import model
from ssl import create_default_context
from statistics import mode
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200)
    PRN = models.CharField(max_length = 100)
    description = models.CharField(null = True, blank = True, max_length = 2000)

class Topic(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name



class Notification(models.Model):
    host = models.ForeignKey(User, on_delete = models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null = True, blank=True)
    updates = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updates', '-created']

    def __str__(self):
        return str(self.title)


class Notes(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    link = models.CharField(max_length = 400)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    class Meta:
        ordering = ['-updated', '-created']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0 : 50]
