from rest_framework import serializers
from django.contrib.auth.models import User

class Login(serializers.ModelSerializer):
    class Meta:
        model:User
        fields = ['username', 'password']