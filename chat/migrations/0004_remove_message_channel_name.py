# Generated by Django 4.1.4 on 2022-12-24 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_message_channel_name_alter_message_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='channel_name',
        ),
    ]