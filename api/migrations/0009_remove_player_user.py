# Generated by Django 4.2.7 on 2023-12-17 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_player_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
    ]
