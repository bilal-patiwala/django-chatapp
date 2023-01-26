from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Thread

class Login(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validate_data):
            user =  User.objects.create_user(validate_data['username'], validate_data['email'], validate_data['password'])
            return user

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ThreadSerializer(serializers.ModelSerializer):
    thread = serializers.SerializerMethodField('get_thread_object')
    class Meta:
        model = Thread
        fields = ["sender", "receiver", "id", "thread"]

    def get_thread_object(self, asdada):
        thread_obj = Thread.objects.get(id=asdada.id)
        return thread_obj


class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'