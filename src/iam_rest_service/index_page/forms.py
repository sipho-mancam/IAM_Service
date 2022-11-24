from django import forms



class LoginForm(forms.Form):
    email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    # userId = forms.CharField(max_length=256)



class SignUpForm(forms.Form):
    username = forms.CharField(max_length=255, label='name')
    email = forms.CharField(max_length=255, label='email')
    password = forms.CharField(max_length=255)
    # userId = forms.CharField(max_length=500)
