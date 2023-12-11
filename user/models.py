from django.contrib.auth.models import AbstractUser
from django.db import models

from api.models import Player

class User(AbstractUser):
    player = models.OneToOneField(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name="user")