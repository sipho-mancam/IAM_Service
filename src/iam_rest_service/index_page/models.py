from django.db import models

# Create your models here.


class UserProfile(models.Model):
    name = models.CharField(null=True, max_length=150, blank=True)
    last_name= models.CharField(max_length=150, null=True, blank=True)
    userId = models.TextField(unique=True, blank=True)
    username = models.CharField(max_length=310, null=True, blank=True)
    profile_picture = models.URLField(null=True, blank=True)
    contact_number=models.CharField(max_length=16, null=True, blank=True)
    email = models.EmailField()
    friends = models.JSONField(null=True, blank=True)
    friend_requests = models.JSONField(null=True, blank=True)
    perms = models.JSONField(null=True, blank=True)




def create_user(name, last_name, email, userId, profile_picture, contact=None, friend_requests=None, friends=None, **kwargs):
    user =  UserProfile(name=name, 
                        last_name=last_name, 
                        email=email, 
                        userId=userId, 
                        profile_picture=profile_picture, 
                        contact_number=contact, 
                        friend_requests=friend_requests, 
                        friends=friends)
    user.save()

    return user

def create_user(user_data):
    user=UserProfile(name=user_data.get('name'), 
                    last_name=user_data.get('last_name'), 
                    email=user_data.get('email'), 
                    userId=user_data.get('userId'), 
                    profile_picture=user_data.get('profile_picture'), 
                    contact_number=user_data.get('contact'), 
                    friend_requests=user_data.get('friend_requests'), 
                    friends=user_data.get('friends'))
    user.save()

    return user