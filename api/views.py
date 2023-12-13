import json
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from api.models import CombatList, GameData, Item, Creature, Player, get_draft_list, get_extended_items, get_item_by_tier

from .settings import *
# Create your views here.


'''
game
 charecter
   DONE modifiers
   TODO win/loss
   DONE tier
   TODO round
   DONE gold

   
draft
    DONE buy
    SKIP sell 
    DONE reroll
    DONE list of options

server
    TODO round[charecters]
    TODO update with last opponent or winner?

    TODO getOpponent

combat
    TODO calc combat 
    TODO deteministic combat
'''

def handle_buy_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return JsonResponse({"error":"Not Enough Gold"}, status=400)
        except Item.DoesNotExist:
            return JsonResponse({"error":"Item does not exist"}, status=400)
        except OverflowError:
            return JsonResponse({"error":"Tier maxed"}, status=400)
    return wrapper

def reset(player):
    player.creature.reset()
    player.data.reset()

# ---------------------------------------
# draft 

def JsonUserResponse(request):
    return JsonResponse(request.user.player.serialize())


def JsonModelResponse(list):
    return JsonResponse([item.serialize() for item in list], safe=False)

def draft(request): # list
    request.user.player.update_store_list()
    return JsonModelResponse(request.user.player.data.store_list.all())

@login_required
@require_POST
@handle_buy_error
def buy(request): # gold
    data = json.loads(request.body)

    request.user.player.buyItem(data['id'], data['index'])
    return JsonUserResponse(request)

@login_required
@require_POST
@handle_buy_error
def buy_tier(request):
    request.user.player.buyTier()
    return JsonUserResponse(request)


@login_required
@require_POST
def sell(request): # TODO
    pass

@login_required
@require_POST
@handle_buy_error
def reroll(request):
    request.user.player.reroll()
    return JsonUserResponse(request)

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

def extended_items(request):
    return JsonModelResponse(get_draft_list(1))

def enemy(request):
    return JsonModelResponse(CombatList.objects.all())

def opponent(request, tier):
    CombatList.get_opponent(tier)

    return JsonResponse(CombatList.get_opponent(tier).serialize())

# ---------------------------------------
# Player Setup

def player(request):
    setup(request)
    request.user.player.creature.recalc()
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

    data.update_store_list()