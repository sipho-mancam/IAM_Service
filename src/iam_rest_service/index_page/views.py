from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm
from hashlib import sha256
# Create your views here.


def index(request):
    ua = request.META['HTTP_USER_AGENT']

    if not ('android' in ua.lower() or 'iphone' in ua):
        context = {}
        return render(request, 'index/index-desk.html', context)
    else:
        context = {}
        return render(request, 'index/index-mob.html', context)

    
def email_sign_up(request):

    if request.method == 'POST':
        # it's a post request, let's pull the form data
        form_data = SignUpForm(request.POST)    

        if form_data.is_valid():
            user_data = form_data.cleaned_data
            user_id = sha256(bytes(user_data.__str__(), 'utf-8')).hexdigest()

            # check if user already exist in the DB
            try:
                user = User.objects.get(email=user_data.get('email'), 
                                        username=user_data.get('username'))

                # generate users id and return them
                                        # userId=user_id)
            except User.DoesNotExist as e:
                # user is not found.
                new_user = User.objects.create(email=user_data.get('email'), 
                                        username=user_data.get('username'), 
                                        # userId=user_id, 
                                        password=user_data.get('password'))
                new_user.save()
                # print('User saved Successfully')

            
        else:
            print(form_data.errors.as_json())
            print(form_data.clean())

    return HttpResponse("Thank you for submitting the form")


def email_login(request):

    if request.method =='POST':
        form_obj = LoginForm(request.POST)

        if form_obj.is_valid():
            user_data = form_obj.cleaned_data

            email = user_data.get('email')
            pwd = user_data.get('password')

            try:
                user = User.objects.get(email=email, password=pwd)

                print('user found in the system')
            except User.DoesNotExist as e:
                # user doesn't exist
                print("user doesn't exist")
        else:
            print('something is missing in the form data')

            print(form_obj.errors.as_json())
    else:
        # still to implement get based forms -- probably will just return a security error
        pass
    
    return HttpResponse('Thank you for loging in')
            
        
