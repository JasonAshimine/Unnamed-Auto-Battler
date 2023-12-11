import random
from django.db import models

from api.settings import DRAFT_MAX_SHOW, START_GOLD, START_TIER_COST

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
    # data<GameData> (1)
    # creature<Creature> (1)

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            "name": self.name,
            "data": self.data.serialize(),
            "creature": self.creature.serialize()
        }    

class Item(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    type = models.CharField(max_length=100)
    tier = models.PositiveSmallIntegerField()
    # creatures

    def gen_store_list(self, tier, max = DRAFT_MAX_SHOW):
        items = list(Item.objects.filter(tier__lte=tier))

        if len(items) < max:
            return items
        return random.sample(items, max)

    def serialize(self):
        return {
            "name": self.name,
            "tier": self.tier,
            "type": self.type,
            "value": self.value,
        }
    
    def __str__(self):
        return f"[{self.tier}] {self.name} : {self.type} {self.value}"

class GameData(models.Model):
    wins = models.PositiveSmallIntegerField(default=0)
    loss = models.PositiveSmallIntegerField(default=0)
    round = models.PositiveSmallIntegerField(default=0)
    tier = models.PositiveSmallIntegerField(default=1)
    tier_cost = models.PositiveSmallIntegerField(default=START_TIER_COST)
    gold = models.PositiveSmallIntegerField(default=START_GOLD)

    store_list = models.ManyToManyField(Item, blank=True)

    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name="data")

    def reset(self):
        self.wins = 0
        self.loss = 0
        self.round = 0
        self.tier = 1
        self.tier_cost = START_TIER_COST
        self.gold = START_GOLD
        self.store_list.clear()
    
    def serialize(self):
        return {
            "wins": self.wins,
            "loss": self.loss,
            "round": self.round,
            "tier": self.tier,
            "tier_cost": self.tier_cost,
            "gold": self.gold,
            "store_list": [item.serialize() for item in self.store_list.all()]
        }
    



class Creature(models.Model):
    name = models.CharField(max_length=100)
    max_health = models.PositiveSmallIntegerField()
    defense = models.SmallIntegerField()
    attack = models.SmallIntegerField()

    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name="creature")
    items = models.ManyToManyField(Item, blank=True, related_name="creatures")

    def serialize(self):
        return {
            "name": self.name,
            "health": self.max_health,
            "defense": self.defense,
            "attack": self.attack,
            "items": [item.serialize() for item in self.items.all()]
        }

class CombatList(models.Model):
    creature = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name="combat_list")

    def serialize(self):
        return [creature.serialize() for creature in CombatList.objects.all()]
