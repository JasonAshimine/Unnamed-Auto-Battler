# -------------------------------------
# CONST



from enum import Enum


USER = 'user'
ENEMY = 'enemy'
WINNER = 'winner'
COMBAT_LOG = 'combat_log'


SESSION_STATE = 'state'
SESSION_COMBAT_LOG = 'combat_log'

STATE_COMBAT = 'combat'
STATE_DRAFT = 'draft'

# -------------------------------------
# Draft

DRAFT_MAX_SHOW = 4
MAX_TIER = 6

START_TIER_COST = 5
MIN_TIER_COST = 0

ITEM_COST = 3
REROLL_COST = 1

# -------------------------------------
# Combat

MIN_DAMAGE = 1

COMBAT_START_SCALE = 10
COMBAT_SCALE_INTERVAL = 5
COMBAT_SCALE = 2

COMBAT_MAX_ROUND = 50

# -------------------------------------
# Starting data

START_GOLD = 3
MAX_GOLD = 10

START_CREATURE = {
    "max_health" : 5,
    "defense" : 1,
    "attack" : 1,
    "level" : 0
}

START_GAME_DATA = {
    "wins": 0,
    "loss": 0,
    "round": 0,
    "tier": 1,
    "tier_cost": START_TIER_COST,
    "gold": START_GOLD
}