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

sys.path.append(Path(__file__+'../../../../').resolve().as_posix()+'/helpers/')

# print(sys.path)

from gAuth import *

# Create your views here.
R_URL = 'http://tnds.co.za'

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
                u = UserProfile.objects.get(email=email)
                print(u.get_json_representation())
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
        try:
            # check if user exist in db and then store new user or proceed.
            u_c = User.objects.filter(userId=user_info['id'])
            if len(u_c) > 0:
                for u in u_c:
                    u.delete()
            
            user = User(userId=user_info['id'], 
                        email=user_info['email'], 
                        name=user_info['name'],
                        picture=user_info['picture'])
            user.save()
            id = user_info.get('id')
            ur_l = R_URL + '?userId='+id if id is not None else 'error'
            return redirect(ur_l)
        except Exception as e:
            return HttpResponseServerError('There was an error signing in')
            
        
    elif 'userId' in param:
        # the user exists already in the server
        user = User.objects.filter(userId=param['userId'])
        if len(user)>0:
            u = user[0]
            ob = {}
            ob['name'] = u.name
            ob['email'] = u.email
            ob['pciture'] = u.picture
            ob['userId'] = u.userId
            return HttpResponse(ob.__str__(), content_type='application/json')
        else:
            return HttpResponse({'info':'user not found'}, content_type='application/json')

    elif 'error' in param:
        # return the error message to the source url
        return HttpResponseServerError('There was an error signing in')


    else:
        flow, url = google_authentication_url()
        return redirect(url)

def g_login(request):
    pass