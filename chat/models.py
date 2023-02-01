from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models import Q
from django.conf import settings
# Create your models here.

class UserManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=54, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']



class ThreadManager(models.Manager):
    def get_by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(sender=user) | Q(receiver=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_user")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver_user")
    updated = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    class Meta:
        unique_together = ['sender', 'receiver']

    def __str__(self):
        return f'message between {self.sender.username} and {self.receiver.username}'
    

class Message(models.Model):
    message = models.CharField(max_length=1000000, blank=False)
    user = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True, related_name='message_thread')
    date = models.DateTimeField(auto_now_add=True)
    
    

    