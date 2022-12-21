from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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
    if User.objects.filter(username=username).exists():
        return render(request, "chat/room.html", {'username':username})
    
    return redirect('index')