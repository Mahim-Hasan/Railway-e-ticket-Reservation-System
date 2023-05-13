from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from main.models import *


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    elif request.method == "POST":
        
        username = request.POST["phone"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if request.GET:
                return redirect(request.GET['next'])

            else:
                return redirect('/')

        else:
            messages.error(request, 'Invalid Credentials!')
            return redirect('/user/login')


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')

    elif request.method == "POST":
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        username = request.POST["phone"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, 'Passwords are not same!')
            return redirect('/user/register')


        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Phone number already in used!')
            return redirect('/user/register')

        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Already have an account with this email!')
            return redirect('/user/register')
            
        else:
            user = User.objects.create_user(first_name=firstName, last_name=lastName, username=username, email=email, password=password1)
            user.save()
            return redirect('/user/login')


def logout(request):
    auth.logout(request)
    return redirect("/")
        



