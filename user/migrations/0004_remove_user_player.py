# Generated by Django 4.2.7 on 2023-12-17 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='player',
        ),
    ]
