from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .forms import SignUpForm, LoginForm
from hashlib import sha256
from .models import UserProfile, create_user
import sys
from pathlib import Path
import json
from password_validator import PasswordValidator

sys.path.append(Path(__file__+'../../../../').resolve().as_posix()+'/helpers/')

from gAuth import *


# imports for the restful interface of the app
from rest_framework import viewsets, permissions
from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'userId'


####################################################
# End of the Rest API code here                    #
####################################################


# Create your views here.
R_URL = 'http://tnds.co.za'
password_schema = PasswordValidator()

password_schema.min(8).max(100).has().digits().has().letters().has().symbols().has().lowercase().has().uppercase()


def send_response_to_form(request, context={})->HttpResponse:
    ua = request.META['HTTP_USER_AGENT']
    if not ('android' in ua.lower() or 'iphone' in ua):
        return render(request, 'index/index-desk.html', context)
    else:
        return render(request, 'index/index-mob.html', context)


def index(request):
    ua = request.META['HTTP_USER_AGENT']
    context = {}
    if not ('android' in ua.lower() or 'iphone' in ua):
        return render(request, 'index/index-desk.html', context)
    else:
        return render(request, 'index/index-mob.html', context)

    
def email_sign_up(request):
    if request.method == 'POST':
        # it's a post request, let's pull the form data
        form_data = SignUpForm(request.POST)    

        if form_data.is_valid():
            user_data = form_data.cleaned_data
            # Run validation chains

            # validate the password
            if not password_schema.validate(user_data.get('password')):
                context = {'password':True}

                return send_response_to_form(request, context)

            try:
                # check if email already taken
                User.objects.get(email=user_data.get('email'))
                context = {'error':'User with that email already exist!'}
                return send_response_to_form(request, context)

            except User.DoesNotExist as e:
                # check username if it is already taken.
                try:
                    User.objects.get(username=user_data.get('username'))
                    context = {'error':'User name already taken!'}
                    return send_response_to_form(request, context)
                except Exception as e:
                    new_user = User.objects.create_user(user_data.get('username'), user_data.get('email'), user_data.get('password'))
                    print('User successfully created.')
                    new_user.save() 

                    # Start the flow of creating a user profile and store it.
                    userId = sha256(bytes(user_data.__str__(), 'utf-8')).hexdigest()
                    user_data['userId'] = userId
                    user_data['friends'] = json.encoder.JSONEncoder().encode({'iadas':{'accepted': True}})
                    create_user(user_data)
                    print('User profile created and saved')  
                    return redirect(R_URL+'?userId=%s'%userId)
                    #we redirect the user to the calling website.     
        else:
            context = {'error':f'Invalid data input: {form_data.errors.as_data()}'}
            return send_response_to_form(request, context)


def email_login(request):
    if request.method =='POST':
        form_obj = LoginForm(request.POST)

        if form_obj.is_valid():
            user_data = form_obj.cleaned_data 
            email = user_data.get('email')
            pwd = user_data.get('password')
            
            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist as e:
                # print(e)
                return send_response_to_form(request, {'error':'Invalid Credentials'})

            user = authenticate(username=user, password=pwd)

            if user is None:
                return send_response_to_form(request, {'error':'Invalid Credentials'})
            else:
                # get user id from the user profiles.
                try:
                    u = UserProfile.objects.get(email=email)
                except UserProfile.DoesNotExist as e:

                    userId = sha256(bytes(user_data.__str__(), 'utf-8')).hexdigest()
                    user_data['userId'] = userId
                    user_data['friends'] = json.encoder.JSONEncoder().encode({'iadas':{'accepted': True}})
                    u = create_user(user_data)

                return redirect(R_URL+'?userId=%s'%u.userId)
    else:
        # still to implement get based forms -- probably will just return a security error
        context = {'error':f'Invalid data input: {form_obj.errors.as_data()}'}
        return send_response_to_form(request, context)
            
        
def g_signup(request):
    param = request.GET
    if 'code' in param:
        creds, token = google_fetch_access_code(param['code'])
        user_info = google_user_data(creds=creds)
        # if you are signing up it means that you don't have an account with us yet, let's confirm this.
        # now how this works is that, if I perform a manual login (email style) and then signup with google, 
        # the two accounts must be linked and show consistent information, so one email address can only be 
        # associated with a single profile, we update the information to be based on the latest login method.
        # let's grab the email address and search it in the db.
        email = user_info['email']
        user_info['profile_picture'] = user_info['picture']
        user_info['userId'] = sha256(bytes(user_info['id'], 'utf-8')).hexdigest()

        try:
            u = UserProfile.objects.filter(email=email)
            if len(u) == 0: # you haven't signed up with this email address
                u = create_user(user_info)
                return redirect(R_URL+'?userId=%s'%user_info['userId'])
            else:
                # this means that you are in our database...
                if u[0].userId == user_info['userId']:
                    return redirect(R_URL+'?userId=%s'%user_info['userId'])
                
                u[0].name = user_info['name']
                u[0].userId = user_info['userId']
                u[0].profile_picture = user_info['profile_picture']
                u[0].save()

                print(u[0].name)
                return redirect(R_URL+'?userId=%s'%user_info['userId']) 

        except Exception as e:
            return HttpResponseServerError('Unkown Server Error %s'% e.__str__())

    else:
        flow, url = google_authentication_url()
        return redirect(url)

