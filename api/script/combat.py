import random
from api.settings import *
from api.util import DotDict

def calc_combat(user_creature, opponent):
    user = combat_clone(user_creature)
    enemy = combat_clone(opponent)

    isUserTurn = combat_decide_first(user, enemy)

    list = []
    multiplier = 1
    scale_counter = 0
    winner = None

    for round in range(COMBAT_MAX_ROUND):
        if round >= COMBAT_START_SCALE:
            scale_counter -= 1
            if scale_counter <= 0:
                multiplier *= COMBAT_SCALE
                scale_counter = COMBAT_SCALE_INTERVAL            

        result = calc_combat_round(user, enemy, isUserTurn, multiplier)
        list.append(result)
        
        if result['done']:
            winner = combat_turn_tag(isUserTurn)
            break

        isUserTurn = not isUserTurn

    return [winner, list]

def combat_clone(creature):
    return DotDict(creature.serialize())

def combat_decide_first(user, opponent):
    if user.level > opponent.level:
        return True
    
    if user.level == opponent.level:
        return random.choice([True, False])
    
    return False

def combat_decide_attacker(user, opponent, isUserTurn):
    if isUserTurn:
        attacker = user
        defender = opponent
    else:
        attacker = opponent
        defender = user

    return [attacker, defender]

def calc_combat_round(user, opponent, isUserTurn, multiplier = 1):
    attacker, defender = combat_decide_attacker(user, opponent, isUserTurn)
    damage = calc_combat_damage(attacker, defender, multiplier)

    target = combat_turn_tag(not isUserTurn)

    defender.health -= damage

    return {
        "target": target,
        "damage": damage,
        "health": defender.health,
        "multiplier": multiplier,
        "done": defender.health <= 0
    }

def calc_combat_damage(attack, defender, multiplier):
    damage = attack.attack - defender.defense # TODO improve calc
    return max(damage, MIN_DAMAGE) * multiplier

def combat_turn_tag(isUserTurn):
    if isUserTurn:
        return USER
    return ENEMY