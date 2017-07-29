# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render,redirect
from models import instamodel,SessionToken,PostModel
from forms import SignUpForm,LoginForm, PostForm
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse
from tarnjeet.settings import BASE_DIR

from imgurpython import ImgurClient

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
        hello = SessionToken()
        #hello.check_validation(request)

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
                        response = redirect('/post/')
                        response.set_cookie(key='session_token', value=token.session_token)
                        return response
                    else:
                        print 'User is invalid'


        elif request.method == "GET":
            form = LoginForm()
            return render(request, 'Login.html', {'hello': date}, {'form': LoginForm})


def feed_view(request):
    return render(request, 'feed.html')


def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'GET':
                form = PostForm()
                return render(request, 'post.html', {'form': PostForm})
        elif request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()
                the = str(BASE_DIR+"/")
                path = str(the+ post.image.url)

                client = ImgurClient('ea9c85676333421', '3774d6d792ca8cdc53783a8681b1f8850bed77cf')
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()

                return redirect('/feed/')
            return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')
def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        return render(request,'feed.html',{'posts':posts})
    else:
        return redirect('/login/')

# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None