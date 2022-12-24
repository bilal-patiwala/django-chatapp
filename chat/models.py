from django.db import models
from django.contrib.auth.models import User
import random
import string
# Create your models here.

def getChannelName():
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return key
    

class Message(models.Model):
    message = models.CharField(max_length=1000000, blank=False)
    date = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    
    def __str__(self):
        return f"Message fron {self.sender} to {self.receiver}"
