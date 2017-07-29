from django import forms
from models import instamodel,PostModel

class SignUpForm(forms.ModelForm):
  class Meta:
    model = instamodel
    fields=['email','username','name','password']

class LoginForm(forms.ModelForm):
    class Meta:
        model = instamodel
        fields = ['username', 'password']

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields=['image', 'caption']
