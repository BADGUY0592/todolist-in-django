from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,authenticate,logout
from .forms import TodoForm
from .models import Todo


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
    todos=Todo.objects.filter(User=request.user,datecompleted__isnull=True).order_by('-created')
    return render(request, 'todo/currenttodos.html',{'todos':todos})

def tododetail(request, todo_pk):
    todo = get_object_or_404(Todo, id=todo_pk,User=request.user)
    return render(request, 'todo/tododetails.html',{'todo':todo})

def edittodo(request, todo_pk):
    todo = get_object_or_404(Todo, id=todo_pk, User=request.user)
    if request.method == 'GET':
        form=TodoForm(instance=todo)
        return render(request, 'todo/edittodo.html',{'todo':todo,'form':form})
    elif request.method == 'POST':
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/edittodo.html', {'todo':todo,'form':form,'error':'Value Error.'})

def deltodo(request, todo_pk):
    todo = get_object_or_404(Todo, id=todo_pk,User=request.user)
    form=TodoForm(instance=todo)
    return render(request, 'todo/edittodo.html',{'todo':todo,'form':form})

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html',{'form':TodoForm()})
    elif request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.User = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(),'error':'Value Error.'})