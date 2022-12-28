from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Message, Thread

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if request.method == 'POST':
        if User.objects.filter(username=username).exists():
            messages.error(request, 'user already exist')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            return redirect('index')
    return render(request, 'chat/register.html')

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if request.method == 'POST':
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'chat/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def room(request, username):
    sender = request.user
    thread = Thread.objects.get_by_user(user=sender).prefetch_related('message_thread')
    try:
        receiver = User.objects.get(username=username)
            
    except User.DoesNotExist:
        return redirect('index')

    if thread.exists():
        context = {
            'username':username,
            'sender':sender.username,
            'thread_id':thread.first().id,
            'thread':thread
        }
    else:
        new_thread = Thread.objects.create(sender=sender, receiver=receiver)
        new_thread.save()
        t = Thread.objects.get_by_user(user=sender).prefetch_related('message_thread')
        context = {
            'username':username,
            'sender':sender.username,
            'thread_id':t.first().id,
            'thread':t
        }

    return render(request, "chat/room.html", context)