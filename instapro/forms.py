from django import forms
from models import instamodel

class SignUpForm(forms.ModelForm):
  class Meta:
    model = instamodel
    fields=['email','username','name','password']

class LoginForm(forms.ModelForm):
    class Meta:
        model = instamodel
        fields = ['username', 'password']