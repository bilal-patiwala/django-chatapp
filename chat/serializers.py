from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import User
from django.conf import settings
from .models import Thread, Message

class Login(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validate_data):
            user =  User.objects.create_user(validate_data['email'], validate_data['username'], validate_data['password'])
            return user

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ThreadSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(source='sender.username', read_only=True)  
    receiver = serializers.PrimaryKeyRelatedField(source='receiver.username', read_only=True)
    class Meta:
        model = Thread
        fields = ["sender", "receiver", "id", ]

    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message', 'user', 'thread','date']
    

    


class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'