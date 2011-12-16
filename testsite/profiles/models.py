from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    bio = models.TextField()

class Contact(models.Model):
    owner = models.ForeignKey(Profile)
    mean = models.CharField(max_length=16)
    data = models.CharField(max_length=255)
