# Generated by Django 4.1.4 on 2022-12-23 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message_channel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='channel_name',
            field=models.CharField(default='HFG6IBhR1LtLJXFT', max_length=16),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(max_length=1000000),
        ),
    ]
