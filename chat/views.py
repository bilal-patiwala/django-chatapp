from django.shortcuts import redirect, render
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Message, Thread
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, SearchSerializer, ThreadSerializer, UserProfileSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication, default_user_authentication_rule
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework.settings import api_settings
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
User = get_user_model()



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    print(data)
    serializer = RegisterSerializer(data=data)
    print(serializer.is_valid())
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

# @api_view(['POST'])
# def login(request):
#     data = request.data
#     username = data.username
#     password = data.password

@api_view(['GET'])
@permission_classes((AllowAny, ))
@authentication_classes([JWTAuthentication])
def searchUser(request, searchText):
    querySet = User.objects.filter(username__startswith=searchText)[:5]
    serializer = SearchSerializer(querySet, many=True)
    return Response(serializer.data)

class GetThread(APIView):
    permission_classes = (AllowAny, )
    authentication_classes = (JWTAuthentication, )
    def get(self, request, username):
        t1 = request.headers.get('Authorization').split()
        t = t1[1].split('}')
        print(t[0])
        access_token_obj = RefreshToken(t[0], verify=True)
        u=access_token_obj['username']
        sender=User.objects.get(username=u)
        s=sender
        receiver = User.objects.get(username=username)
        print(sender)
        thread = Thread.objects.get_by_user(user=sender).prefetch_related('message_thread')
        print(thread.first().receiver)
        if thread.exists():
            print("exist")
            context = {
                'sender':sender,
                'receiver':receiver,
                'id':thread.first().id,
            }
        else:
            print("not exist")
            new_thread = Thread.objects.create(sender=sender, receiver=receiver)
            new_thread.save()
            th = Thread.objects.get_by_user(user=sender).prefetch_related('message_thread')
            context = {
                'sender':sender,
                'receiver':receiver,
                'id':th.first().id,
            }

        print(context)
        print("okk..")
        serializer = ThreadSerializer(context)
        print("okk...1")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
  permission_classes = [AllowAny]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class GetMessages(APIView):
    permission_classes = (AllowAny, )
    authentication_classes = (JWTAuthentication, )
    def get(self, request):
        print("hello")
        print(request)
        t1 = request.headers.get('Authorization').split()
        print("hello")
        t = t1[1].split('}')
        print(t[0])
        access_token_obj = RefreshToken(t[0], verify=True)
        u=access_token_obj['username']
        sender=User.objects.get(username=u)
        print(sender.id)
        messages = Message.objects.filter(user=sender)
        print("............here come thread id ...............")
        print(messages.first().thread.id)
        allMessages = Message.objects.filter(thread=messages.first().thread)
        serializer = MessageSerializer(allMessages, many=True)
        return Response(serializer.data)
    
class GetAllUserAlreadyHasConv(APIView):
    permission_classes = (AllowAny, )
    authentication_classes = (JWTAuthentication, )
    def get(self, request):
        t1 = request.headers.get('Authorization').split()
        print("hello")
        t = t1[1].split('}')
        print(t[0])
        access_token_obj = RefreshToken(t[0], verify=True)
        u=access_token_obj['username']
        sender=User.objects.get(username=u)
        

