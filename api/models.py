import random
from django.db import models

from .settings import *

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

def get_draft_list(tier):
    items = list(Item.objects.filter(tier__lte=tier))

    if len(items) < DRAFT_MAX_SHOW:
        return items
    return random.sample(items, DRAFT_MAX_SHOW)


class UpdateMixin:
    def update(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.save()

class Player(models.Model):
    name = models.CharField(max_length=100)
    # data<GameData> (1)
    # creature<Creature> (1)

    def buyTier(self):
        self.data.buyTier()

    def buyItem(self, id):
        item = self.data.buyItem(id)
        self.creature.add(item)
        self.save_all()
        return item
        
    def reroll(self):
        self.data.reroll()

    def reset(self):
        self.data.reset()
        self.creature.reset()

    def save_all(self):
        self.data.save()
        self.creature.save()

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
            "id":self.id,
            "name": self.name,
            "tier": self.tier,
            "type": self.type,
            "value": self.value,
        }
    
    def __str__(self):
        return f"[{self.tier}] {self.name} : {self.type} {self.value}"

class GameData(UpdateMixin, models.Model):
    wins = models.PositiveSmallIntegerField(default=0)
    loss = models.PositiveSmallIntegerField(default=0)
    round = models.PositiveSmallIntegerField(default=0)
    tier = models.PositiveSmallIntegerField(default=1)
    tier_cost = models.PositiveSmallIntegerField(default=START_TIER_COST)
    gold = models.PositiveSmallIntegerField(default=START_GOLD)

    store_list = models.ManyToManyField(Item, blank=True)

    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name="data")

    def buyTier(self):
        if self.tier >= MAX_TIER:
            raise OverflowError

        self.spend(self.tier_cost)
        self.tier += 1
        self.tier_cost = START_TIER_COST + self.tier
        self.save()

    def buyItem(self, id):
        self.spend(ITEM_COST)        
        return self.remove_item(id)
    
    def reroll(self):
        self.spend(REROLL_COST)
        self.update_store_list()
        self.save()

    def spend(self, cost):
        if self.gold < cost:
            raise ValueError
        self.gold -= cost
    
    def update_store_list(self):
        self.store_list.set(get_draft_list(self.tier))

    def remove_item(self, id):
        item = self.store_list.get(pk=id)
        self.store_list.remove(item)

        return item

    def reset(self):
        self.update(**START_GAME_DATA)
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
    



class Creature(UpdateMixin, models.Model):
    name = models.CharField(max_length=100)
    max_health = models.PositiveSmallIntegerField()
    defense = models.SmallIntegerField()
    attack = models.SmallIntegerField()

    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name="creature")
    items = models.ManyToManyField(Item, blank=True, through='CreatureItemCount')

    def add(self, item):
        obj, created = CreatureItemCount.objects.get_or_create(creature=self, item=item)
        if not created:
            obj.count += 1
            obj.save()

    def reset(self):
        self.update(**START_CREATURE)
        self.items.clear()

    def serialize(self):
        return {
            "name": self.name,
            "health": self.max_health,
            "defense": self.defense,
            "attack": self.attack,
            "items": [item.serialize() for item in self.counts.order_by('item__tier', 'item__type', 'item__name').all()]
        }
    
class CreatureItemCount(models.Model):
    creature = models.ForeignKey(Creature, on_delete=models.CASCADE, related_name='counts')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.SmallIntegerField(default=1)

    def serialize(self):
        return {
            **self.item.serialize(),
            "count": self.count
        }

class CombatList(models.Model):
    creature = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name="combat_list")

    def serialize(self):
        return self.creature.serialize()
