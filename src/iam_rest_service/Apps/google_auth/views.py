import sys
from pathlib import Path
sys.path.append(Path(__file__+'../../../../../').resolve().as_posix()+'/helpers/')
from django.shortcuts import render
from gAuth import *
from django.http import HttpResponse, HttpRequest

# Create your views here.

flow_o = None

def login(request):
    global flow_o
    param = request.GET

    if 'code' in param:
        creds, token = google_fetch_access_code(param['code'])
        user_info = google_user_data(creds=creds)
        
        print(user_info)
        # check if user exist in db and then store new user or proceed.
    elif 'userId' in param:
        # the user exists already in the server
        pass    

    else:
        flow, url = google_authentication_url()
        flow_o = flow
        print(url)
    return HttpResponse("Hello world")

    