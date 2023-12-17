# Unamed Auto Battler Game

## Distinctiveness and Complexity
Originally designed for allow RESTful autobattler game inspired by "Super Auto Pets" with multiplayer by storing users at their round and resending as opponent to next player.
Unfortunately, project feature creep grew too much for available time and mulitplayer feature was cut for random enemies.

 - Created a web based auto battler game.
 - Animated Pixel sprites / combat with event based sequencing.
 - Game loop is Drafting then Combat with Randomly generated enemies.
 - Item tier system, tier leveling system and scaling tier cost.
 - Randomly generated shop with scaling item rarity based on tier.
 - Speed control to accelerate animations (Makes combat faster).
 - Uses API interface to update client in SPA style.

## How to run.
 - No Additonal packages. Tried to build using only native django, HTML, JavaScript, Bootstrap and CSS (Sass).
 - Start server & register user to begin playing.

## How to play
### Draft
 - Items cost 3 gold. Reroll cost 1 gold.
 - Tier cost decreases every turn & reset cost (new tier + 1) when bought.
 - Items scale with tier upto 5 and become rarer higher tier.
 - Starting gold increases every turn till 10.

 ### Combat
 - Level is based on sum of item tiers. 
 - Combat calc is simple Attack - Defense (min 1 damage).
 - Highest level goes first. On ties random.
 - Combat damage doubles after 10 rounds then keeps doubling every 5 rounds after.
 
*Can "Retire" Run i.e. Reset Run with topright button*
*Combat is resolved determinsitcally and at end of draft. Would allow implementing async multiplayer later*

## Files
### API
Back End: Game Logic scripts / player creation.

##### Models: builtin serialize
   - Player: main interface for GameData, Creature.
   -- interface for buying item, tier, reroll, reset

   - ItemType: Type of bonus, Display Icon, and Name
   - Item: Type, Tier, and bonus value

   - GameData: wins, loss, round, gold, tier, tier cost, shop, and gold.
   *store_list is stored a json to allow duplicates. SQLite doesnt allow arrays*
   -- interface for buying item, tier, reroll, reset, spend(gold), new store list, remove item
    
   - Creature: max_health, defense, attack, level
   -- interface for calc item(update stats), recalc(recalc all), add(item), addRandomItem, reset
   
   - CreatureItem: Item with count qty. Better visual for user / avoids recounting. 
   *Allows duplicate items via count*
  
   - CombatList: Enemy List of creatures. 
   *Originally store user data here to be pulled later. Currently using random generated monster.*
 - Test Cases for Models

##### View.py : Manages gamestate and Enemy data.
API responses via json data. (Serialized via model.serialize)
 - API POST: buy, buy_tier, reroll, endTurn, endCombat, retire
 - INFO GET: player, creature, gamedata, enemy, opponent/tier, item, item/extend(full list with tier)

### Main
Front End: Templates, components, CSS, and JavaScript.
 - img: free sprite sheets from online

#### Animation
 - sprite-animation.scss: animations for sprites (idle, attack, death)
 - icons.scss: uses icon sheet to render mulitple icons via class
 - anim-damage.scss: animation for damage number above sprite
 - style.scss: general formatting / speed variable / hides components based on game state

#### JavaScript
 - script.js: main API handler / updates HTML
   - updates HTML with JSON response data 
 - combat.js: animates combat between sprites.
   - Uses promisfied animationend/transistionend triggers to sequence combat turns.

#### Templates
 - Components: 
   - combat.html: Combat sprite, Health bar, stats
   - creature.html: list of items. (Cut stats in favor for on sprite)
   - data.html: game data render: rounds, wins, loss, tier, tier cost, gold, shop.
   - item.html: item data w/optional buy button & count
   - sprite.html: sprite container & stats
   *Change sprite by changing dataset: tag (Enemy Tag) and type (idle, attack, death)*
 - layout.html: Basic overarching layout
 - index.html: contains components and game state for formatting
 - view.py
   - basic index render using json from API
 
### User
 - Basic user model with reference to Player Model
   *had to add User mananager to fix issues with registration*
 - Reused Login / Register script & templates from previous projects