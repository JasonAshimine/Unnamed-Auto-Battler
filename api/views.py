import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from api.script.combat import calc_combat

from api.models import CombatList, GameData, Item, Creature, Player, get_draft_list, get_extended_items, get_item_by_tier

#from api.combat import calc_combat

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
def get_session_data(request):
    state = request.session.get(SESSION_STATE, None)
    if state == STATE_COMBAT:
        return request.session.get(SESSION_COMBAT_LOG, None)
    
    return None

def get_full_user_data(request):
    if request.user.player is None:
        setup(request.user)

    user_data = request.user.player.serialize()
    user_data['state'] = request.session.get(SESSION_STATE, DEFAULT_STATE)

    session_data = get_session_data(request)
    if session_data:
        user_data.update(session_data)
    
    return user_data

def JsonUserResponse(request, data = None):
    user_data = get_full_user_data(request)

    if data:
        user_data.update(data)
        
    return JsonResponse(user_data)

def JsonModelResponse(list):
    return JsonResponse([item.serialize() for item in list], safe=False)

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
def sell(request): # TODO - Skip?
    pass

@login_required
@require_POST
@handle_buy_error
def reroll(request):
    request.user.player.reroll()
    return JsonUserResponse(request)

@login_required
@require_POST
def end_combat(request):
    request.session[SESSION_STATE] = STATE_DRAFT
    request.session[SESSION_COMBAT_LOG] = None

    return JsonUserResponse(request)


@login_required
@require_POST
def end_draft(request): # TODO - return combat data and update new round & winner/loss
    player = request.user.player
    opponent = CombatList.get_opponent(player.data.round)

    winner, combat_log = calc_combat(player.creature, opponent)

    combat_data = {
        COMBAT_LOG: combat_log, 
        WINNER:winner,
        ENEMY: opponent.serialize()
    }

    end_update_player(player, winner)
    request.session[SESSION_STATE] = STATE_COMBAT
    request.session[SESSION_COMBAT_LOG] = combat_data

    return JsonUserResponse(request)


def end_update_player(player, winner):
    data = player.data

    data.round += 1
    data.tier_cost = max(MIN_TIER_COST, data.tier_cost - 1)
    data.gold = min(MAX_GOLD, START_GOLD + data.round)
    

    if winner is USER:
        data.wins += 1
    elif winner is ENEMY:
        data.loss += 1
        
    data.new_store_list()
    data.save()

@login_required
@require_POST
def retire(request):
    reset(request.user.player)
    request.session[SESSION_STATE] = DEFAULT_STATE
    return JsonUserResponse(request)

# ---------------------------------------
# Server

def get_opponent(request):
    round = request.user.player.data.round
    return CombatList.get_opponent(round)

def end_round(player):
    pass

# ---------------------------------------
# Combat

def combat(request):
    user = request.user.player.creature
    enemy = get_opponent(request)

    winner, combat_log = calc_combat(user, enemy)

    return JsonResponse({
        WINNER: winner,
        COMBAT_LOG:combat_log
        }, safe=False)

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
    return JsonResponse(CombatList.get_opponent(tier).serialize())


# ---------------------------------------
# Player Setup

def player(request):
    setup(request.user)
    request.user.player.creature.recalc()
    return JsonUserResponse(request)


def setup(user):
    if user.player is None:
        create_player(user)


def create_player(user):
    player = Player.objects.create(name=user.username)
    create_game_data(player)
    

def create_game_data(player):
    Creature.objects.create(player=player, **START_CREATURE)
    data = GameData.objects.create(player=player,**START_GAME_DATA)

    data.new_store_list()
    data.save()