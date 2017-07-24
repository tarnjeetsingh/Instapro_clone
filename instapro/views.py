# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render,redirect
from models import instamodel,SessionToken
from forms import SignUpForm,LoginForm
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse

# Create your views here.
def signup_view(request):
    date = datetime.now()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = instamodel(name=name,password=make_password(password),email=email,username=username)
            user.save()
            return render(request,'success.html')

    elif request.method == "GET":
        form = SignUpForm()
        return render(request, 'index.html', {'hello': date}, {'form': SignUpForm})

def login_view(request):
        date = datetime.now()
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = instamodel.objects.filter(username=username).first()

                if user:
                    # Check for the password
                    if check_password(password, user.password):
                        print 'User is valid'
                        token = SessionToken(user=user)
                        token.create_token()
                        token.save()
                        response = redirect('feed/')
                        response.set_cookie(key='session_token', value=token.session_token)
                        return response
                    else:
                        print 'User is invalid'


        elif request.method == "GET":
            form = LoginForm()
            return render(request, 'Login.html', {'hello': date}, {'form': LoginForm})