from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
# Create your models here.

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
    
    
