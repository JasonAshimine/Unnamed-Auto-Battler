const SPRITE_ENEMY = {};
const SPRITE_USER = {};

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
});


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
    document.querySelectorAll('#speed button').forEach(e => e.classList.remove('active'));
    element.classList.add('.active');
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

    return fetchHandler('/api/endCombat/').then(() => resetCombat());
}


async function startCombat(){
    const res = await fetchCSRF('api/player/');
    const data = await res.json();

    console.log(data);

    SPRITE_ENEMY.maxHP = data.enemy.health;
    SPRITE_USER.maxHP = data.creature.health;

    for(item of data.combat_log){
        await animateCombatRound(item);
    }    
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
    idleSprite(SPRITE_ENEMY.sprite);
    idleSprite(SPRITE_USER.sprite);
    SPRITE_ENEMY.element.classList.remove('hide');
    document.querySelectorAll('#combat-buttons button:disabled').forEach(e => e.disabled = false);
}