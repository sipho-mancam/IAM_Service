from django.db import models

# Create your models here.

class User(models.Model):
    userId = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    picture = models.URLField()
