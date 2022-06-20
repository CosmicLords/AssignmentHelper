from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name



class Notification(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True)
    title = models.CharField(max_length=200)
    description = models.TextField(null = True, blank=True)
    updates = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updates', '-created']

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0 : 50]

    