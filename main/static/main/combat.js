const SPRITE_ENEMY = {};
const SPRITE_USER = {};
var _CombatState = null;

document.addEventListener("DOMContentLoaded", () => {
    const combat = document.querySelector('#combat');

    combat.querySelectorAll(".damage").forEach(element => {
        element.addEventListener('animationend', () => {
            element.style.animationPlayState = 'paused';
        });
    });

    combat.querySelectorAll('#speed button').forEach(element => {
        element.onclick = () => handleSpeedClick(element);        
    });

    const setState = state => combat.dataset.state = state;

    combat.querySelector('#start-combat').onclick = (ev) => {
        if(combat.dataset.state == 'combat') return;

        let element = ev.target;

        element.disabled = true;
        setState('combat');
        startCombat().then(() => element.disabled = false);
    }
    combat.querySelector('#end-combat').onclick = () => {
        setState('wait');
        endCombat();
    }


    genSpriteConst(SPRITE_ENEMY, '#combat .enemy');
    genSpriteConst(SPRITE_USER, '#combat .user');
    
    if(document.querySelector('#game').dataset.state == 'combat')
        startCombat();
});

const ENEMY_LIST = [
    'rat',
    'slime',
    'pebble',
    'bat',
    'crab',
    'bones',    
    'golem'   
];

function onCombatEnter(){
    console.log('onEnter');
    startCombat();
}


function chooseEnemy(round){
    tag = ENEMY_LIST[(round-1)%ENEMY_LIST.length];
    SPRITE_ENEMY.sprite.dataset.tag = tag;
}


//Initialize element reference
function genSpriteConst(obj, parentQuery){
    parent = document.querySelector(parentQuery);
    obj.element = parent;
    obj.hp = parent.querySelector('.progress-bar');
    obj.sprite = parent.querySelector('.sprite');
    obj.damage = parent.querySelector('.damage');
}

//Speed handler

function setSpeed(val){  document.documentElement.style.setProperty('--speed', val); }
function handleSpeedClick(element){
    setSpeed(element.dataset.speed);
    document.querySelectorAll('#speed .active').forEach(e => e.classList.remove('active'));
    element.classList.add('active');
}

/* -----------------------------------------
Combat handlers:
 ----------------------------------------- */

async function endCombat(){
    SPRITE_USER.hp.style.width = '100%';
    SPRITE_ENEMY.element.addEventListener

    await new Promise(res => {
        SPRITE_ENEMY.element.addEventListener('animationend', res, {once: true});
        SPRITE_ENEMY.element.classList.add('hide');
    });

    await fetchHandler('/api/endCombat/');
    resetCombat();
}


async function startCombat(){
    const res = await fetchCSRF('api/player/');
    const data = await res.json();

    resetCombat();
    chooseEnemy(data.data.round);
    _CombatState = data.data.round;

    document.querySelector('#start-combat').disabled = true;
    SPRITE_ENEMY.maxHP = data.enemy.health;
    SPRITE_USER.maxHP = data.creature.health;

    for(item of data.combat_log){
        if(_CombatState != data.data.round)
            return;
        await animateCombatRound(item);
    }

    document.querySelector('#combat').dataset.state = 'wait';
    document.querySelectorAll('#combat-buttons button:disabled').forEach(e => e.disabled = false);
}

function determineTarget(target){
    if(target == 'user')
        return [SPRITE_ENEMY, SPRITE_USER];

    if(target == 'enemy')
        return [SPRITE_USER, SPRITE_ENEMY];

    throw new Error(`Invalid target ${target}`);
}

/* -----------------------------------------
Animations:
 ----------------------------------------- */

async function animateCombatRound(roundData){
    const {target, damage, health, multiplier, done} = roundData;
    const [attacker, defender] = determineTarget(target);

    await playSprite(attacker.sprite, 'attack');
    idleSprite(attacker.sprite);
    const animHP = playHP(defender.hp, health, defender.maxHP);
    const animDmg = playDamage(defender.damage, damage, multiplier);

    if(done){
        animHP.then(() => playSprite(defender.sprite, 'death'));
    }

    return Promise.all([animHP, animDmg]);
}

function idleSprite(element){
    element.dataset.type = 'idle';
    resetSprite(element);
}

function resetSprite(element){
    element.style.animationPlayState = 'paused';
    element.style.animation = 'none';
    element.offsetHeight; /* trigger reflow */
    element.style.animation = null;
    element.style.animationPlayState = 'running';
}


function playSprite(element, type){
    return new Promise(res => {
        element.addEventListener('animationend', res, {once: true});
        element.dataset.type = type;
    });
}

function playDamage(element, value, multiplier){
    
    return new Promise(res => {
        element.addEventListener('animationend', () => {
            element.textContent = '';
            res();
        }, {once: true});
        text = value;
        if(multiplier != 1)
            text += ` (x${multiplier})`;
        element.textContent = text;
        resetSprite(element);
    });
}

function playHP(element, partialValue, totalValue){
    const percent = percentage(partialValue, totalValue);
    return new Promise(res => {
        element.addEventListener('transitionend', res, {once: true});
        element.style.width = percent;
    });
}

function percentage(partialValue, totalValue) {
    const val = ((partialValue / totalValue) * 100).toFixed(2);
    return Math.max(0, val) + "%";
}

function resetCombat(){
    SPRITE_ENEMY.hp.style.width = '100%';
    SPRITE_USER.hp.style.width = '100%';

    _CombatState = null;

    idleSprite(SPRITE_ENEMY.sprite);
    idleSprite(SPRITE_USER.sprite);
    SPRITE_ENEMY.element.classList.remove('hide');
    document.querySelectorAll('#combat-buttons button:disabled').forEach(e => e.disabled = false);
}

