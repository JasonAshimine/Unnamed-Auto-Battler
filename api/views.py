import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers

from api.models import CombatList, GameData, Item, Creature, Player

from .settings import *
# Create your views here.


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

TODO create simple user data
TODO buy/sell
TODO List: reroll
TODO create items
TODO 
'''

def reset(player):
    player.creature.reset()
    player.data.reset()


# ---------------------------------------
# draft 

def JsonModelResponse(list):
    return JsonResponse([item.serialize() for item in list], safe=False)

def draft(request): # list
    request.user.player.update_store_list()
    return JsonModelResponse(request.user.player.data.store_list.all())

def buy(request, id): # gold
    item = request.user.player.buy(id)
    return JsonResponse(request.user.player.serialize())

def sell(request): # gold
    pass

def reroll(request): # list
    pass


def get_option_list(tier):
    items = list(Item.objects.filter(tier__lte=tier))

    if len(items) < DRAFT_MAX_SHOW:
        return items
    return random.sample(items, DRAFT_MAX_SHOW)

# ---------------------------------------
# Server

def get_opponent(request):
    pass 

# handle update list

# ---------------------------------------
# Combat

def calc_combat():
    pass



# ---------------------------------------
# Get Data

def creature(request):
    return JsonModelResponse(Creature.objects.all())

def gamedata(request):
    return JsonModelResponse(GameData.objects.all())

def item(request):
    return JsonModelResponse(Item.objects.all())

def enemy(request):
    return JsonModelResponse(CombatList.objects.all())


def player(request):
    setup(request)
    return JsonResponse(request.user.player.serialize())


def setup(request):
    if request.user.player is None:
        create_player(request.user)


def create_player(user):
    player = Player.objects.create(name=user.username)
    Creature.objects.create(player=player, **START_CREATURE)
    data = GameData.objects.create(player=player,**START_GAME_DATA)
    
    user.player = player
    user.save()

    data.store_list.set(get_option_list(1))