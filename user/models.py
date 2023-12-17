from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from api.models import Player

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, player=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    objects = MyUserManager()
    player = models.OneToOneField(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name="user")