import random
from django.db import models
from django.db.models import Max

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

def get_item_by_tier(tier = 1):
    return list(Item.objects.filter(tier__lte=tier))

def num_item_per_tier(tier):
    return MAX_TIER - tier + 1

def get_extended_items(tier = 1):
    items = list(get_item_by_tier(tier))
    extended_items = []
    for item in items:
        extended_items.extend([item] *  num_item_per_tier(item.tier))

    return extended_items

def get_draft_list(tier):
    items = get_extended_items(tier)

    if len(items) < DRAFT_MAX_SHOW:
        return items
    return random.sample(items, DRAFT_MAX_SHOW)

def get_random_item(tier):
    items = get_extended_items(tier)
    index = random.randint(0, len(items)-1)
    return items[index]


class UpdateMixin:
    def update(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.save()

# ------------------------------------------------------------------------------
# Player

class Player(models.Model):
    name = models.CharField(max_length=100)
    # data<GameData> (1)
    # creature<Creature> (1)

    def buyTier(self):
        self.data.buyTier()

    def buyItem(self, id, index):
        item = self.data.buyItem(index)
        if item['id'] != id:
            raise Item.DoesNotExist

        item = Item.objects.get(pk=id)
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

# ------------------------------------------------------------------------------
# Item

class ItemType(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    def serialize(self):
        return self.type

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    tier = models.PositiveSmallIntegerField()
    # creatures

    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, related_name="items")

    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "tier": self.tier,
            "type": self.type.serialize(),
            "value": self.value,
        }
    
    def __str__(self):
        return f"[{self.tier}] {self.name} : {self.type} {self.value}"   

# ------------------------------------------------------------------------------
# Game Data

class GameData(UpdateMixin, models.Model):
    wins = models.PositiveSmallIntegerField(default=0)
    loss = models.PositiveSmallIntegerField(default=0)
    round = models.PositiveSmallIntegerField(default=0)
    tier = models.PositiveSmallIntegerField(default=1)
    tier_cost = models.PositiveSmallIntegerField(default=START_TIER_COST)
    gold = models.PositiveSmallIntegerField(default=START_GOLD)

    #store_list = models.ManyToManyField(Item, blank=True)
    store_list = models.JSONField(default=list)

    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True, related_name="data")

    def buyTier(self):
        if self.tier >= MAX_TIER:
            raise OverflowError

        self.spend(self.tier_cost)
        self.tier += 1
        self.tier_cost = START_TIER_COST + self.tier
        self.save()

    def buyItem(self, index):
        self.spend(ITEM_COST)        
        return self.remove_item(index)
    
    def reroll(self):
        self.spend(REROLL_COST)
        self.update_store_list()
        self.save()

    def spend(self, cost):
        if self.gold < cost:
            raise ValueError
        self.gold -= cost
    
    def update_store_list(self):
        list = get_draft_list(self.tier)
        self.store_list = [item.serialize() for item in list]

    def remove_item(self, index):
        return self.store_list.pop(index)

    def reset(self):
        self.update(**START_GAME_DATA)
    
    def serialize(self):
        return {
            "wins": self.wins,
            "loss": self.loss,
            "round": self.round,
            "tier": self.tier,
            "tier_cost": self.tier_cost,
            "gold": self.gold,
            "store_list": self.store_list
        }
    
# ------------------------------------------------------------------------------
# Creature

class Creature(UpdateMixin, models.Model):
    name = models.CharField(max_length=100, blank=True)
    max_health = models.PositiveSmallIntegerField()
    defense = models.SmallIntegerField()
    attack = models.SmallIntegerField()
    level = models.PositiveIntegerField()

    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name="creature", null=True, blank=True)
    items = models.ManyToManyField(Item, blank=True, through='CreatureItemCount')

    def calc_item(self, item, count=1):
        id = item.type.type
        value = getattr(self, id) + count * item.value
        setattr(self, id, value)
        self.level += item.tier * count

    def recalc(self):
        self.update(**START_CREATURE)
        for data in self.counts.all():
            self.calc_item(data.item, data.count)
        self.save()

    def add(self, item):
        obj, created = CreatureItemCount.objects.get_or_create(creature=self, item=item)
        self.calc_item(item)
        if not created:
            obj.count += 1
            obj.save()

    def addRandomItem(self, tier, count = 1):
        for index in range(count):
            self.add(get_random_item(tier))
        self.save()

    def reset(self):
        self.update(**START_CREATURE)
        self.items.clear()

    def serialize(self):
        return {
            "name": self.name,
            "level": self.level,
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
    
# ------------------------------------------------------------------------------
# Enemy List

class CombatList(models.Model):
    creature = models.OneToOneField(Creature, on_delete=models.CASCADE, related_name="combat_list", blank=True, null=True)

    @staticmethod
    def get_opponent(rank):
        combat, created = CombatList.objects.get_or_create(pk=rank)
        creature = combat.creature

        if created or creature == None:
            creature = Creature.objects.create(combat_list=combat, name=f"Auto {rank}", **START_CREATURE)
            combat.creature = creature
            combat.save()
            creature.addRandomItem(rank, rank)

        return creature

    def serialize(self):
        return self.creature.serialize()
