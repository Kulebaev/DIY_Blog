from django.db import models
from django.contrib.auth.models import User
import datetime

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class UserPost(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=datetime.datetime.now)
    name = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=datetime.datetime.now)
    name = models.CharField(max_length=100, blank=True)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name