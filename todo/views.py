from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, authenticate , logout


# Create your views here.
def home(request):
    return render(request, 'todo/home.html')

def loginuser(request):
    if request.method =='GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    elif request.method == 'POST':
        #check data
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(),'error':'User not Found'})
        else:
            login(request, user)
            return redirect('currenttodos')

def signupuser(request):
    if request.method =='GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    elif request.method =='POST':
        #save data
        if request.POST['password1'] == request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                #username already exists
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(),'error':'Username error already exists.'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(),'error':'Passwords did not match.'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def currenttodos(request):
    return render(request, 'todo/currenttodos.html')