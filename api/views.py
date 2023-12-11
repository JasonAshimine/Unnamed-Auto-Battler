import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers

from api.models import GameData, Item, Creature, Player

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

def reset(request):
    pass

# ---------------------------------------
# draft 

def JsonModelResponse(list):
    return JsonResponse([item.serialize() for item in list], safe=False)

def draft(request): # list
    tier = request.GET.get('tier', 1)
    return JsonModelResponse(get_option_list(tier))

def buy(request): # gold
    pass

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

def player(request):
    setup(request)

    return JsonResponse(request.user.player.serialize())


def setup(request):
    if request.user.player is None:
        create_player(request.user)


def create_player(user):
    player = Player.objects.create(name=user.username)
    Creature.objects.create(player=player, **START_CREATURE)
    GameData.objects.create(player=player, **START_GAME_DATA)