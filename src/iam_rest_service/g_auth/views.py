import sys
from pathlib import Path
sys.path.append(Path(__file__+'../../../../').resolve().as_posix()+'/helpers/')
from django.shortcuts import render, redirect
from gAuth import *
from django.http import HttpResponse, HttpResponseServerError
from .models import User

# Create your views here.
R_URL = 'http://tnds.co.za'

flow_o = None

def signin(request):
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


def login(request):
    pass