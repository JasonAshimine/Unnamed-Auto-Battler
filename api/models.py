from django.db import models

# Create your models here.
'''
game
 charecter
   modifiers
   win/loss
   tier?
   round
   gold

   
draft
    buy
    sell
    reroll
    list of options

server
    round[charecters]
    update with last opponent or winner?

    getOpponent

combat
    calc combat 
    deteministic combat
'''

class Player(models.Model):
    name = models.CharField(max_length=100)
    # GameData (1)
    # Creature (1)

class Item(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    type = models.CharField(max_length=100)
    tier = models.PositiveSmallIntegerField()
    # creatures

    def serialize(self):
        return {
            "name": self.name,
            "tier": self.tier,
            "type": self.type,
            "value": self.value,
        }

class GameData(models.Model):
    gold = models.PositiveSmallIntegerField()
    wins = models.PositiveSmallIntegerField()
    loss = models.PositiveSmallIntegerField()
    round = models.PositiveSmallIntegerField()
    tier = models.PositiveSmallIntegerField()
    tier_cost = models.PositiveSmallIntegerField()

    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name="data")

class Creature(models.Model):
    name = models.CharField(max_length=100)
    max_health = models.PositiveSmallIntegerField()
    defense = models.SmallIntegerField()
    attack = models.SmallIntegerField()

    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name="creature")
    items = models.ManyToManyField(Item, blank=True, related_name="creatures")

class CombatList(models.Model):
    creature = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name="combat_list")