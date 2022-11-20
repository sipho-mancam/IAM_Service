from django.db import models

# Create your models here.
class User(models.Model):
    userId = models.CharField('userId',max_length=250)
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=255)
    picture = models.URLField()
