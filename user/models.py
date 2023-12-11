from django.contrib.auth.models import AbstractUser
from django.db import models

from api.models import Player

class User(AbstractUser):
    player = models.OneToOneField(Player, on_delete=models.DO_NOTHING, null=True, blank=True)