from django.contrib import admin
from .models import Message, Thread
# Register your models here.

admin.site.register(Message)

class Message(admin.TabularInline):
    model = Message

class ThreadAdmin(admin.ModelAdmin):
    inlines = [Message]
    class Meta:
        model=Thread

admin.site.register(Thread, ThreadAdmin)