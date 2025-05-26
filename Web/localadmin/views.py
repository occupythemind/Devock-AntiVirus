from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pathlib import Path
import subprocess


def home(request):
    '''Admin Panel'''
    return render(request, 'localadmin/home.html')

def auth(request):
    '''Login inorder to access admin panel'''
    if request.user.is_authenticated:
        return redirect('localadmin:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('localadmin:home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'localadmin/login.html')

@login_required
def logs(request, num):
    '''Logs of the system
    Display ```num``` number of logs'''
    try:
        with open(f'{Path.cwd()}/devock.log', 'r') as log_file:
            logs = log_file.readlines()
        logs = [log.strip() for log in logs]
    except FileNotFoundError:
        logs = []
    # Reverse the logs to show the latest logs first
    logs.reverse()
    # Get the last num logs
    logs = logs[:num]
    # Render the logs in the template
    context = {'logs': logs, 'num': num}
    # Render the logs in the template
    return render(request, 'localadmin/logs.html', context)

@login_required
def all_users(request):
    '''This will show all users'''
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'localadmin/users.html', {'users':users})

@login_required
def view_processes(request):
    '''This will give all processes in the system'''
    # Get all processes in the system
    processes = subprocess.check_output(['ps', 'aux']).decode('utf-8').split('\n')
    head = processes.pop(0)
    return render(request, 'localadmin/processes.html', {'processes': processes, 'head': head})

@login_required
def info_user(request, id):
    '''This will give info about the user'''
    iuser = User.objects.get(id=id)
    info = iuser.__dict__
    return render(request, 'localadmin/iuser.html', {'info':info, 'iuser':iuser})
    

@login_required
def user_logout(request):
    '''Logout the user'''
    logout(request)
    return redirect('localadmin:home')

@login_required
def read_the_docs(request):
    '''Read the docs'''
    return render(request, 'localadmin/docs.html')
