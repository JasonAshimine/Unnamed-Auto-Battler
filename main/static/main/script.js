var _isModal = false;

document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener('click', event => {
        if(event.target.id == "error")
            return event.target.textContent = '';

        if(_isModal & event.target.classList.contains('modal'))
            return dismissModal();
            
        if(event.target.nodeName !== 'BUTTON')
            return;

        switch(event.target.name){
            case 'buy': return handleBuy(event.target);
            case 'reroll': return handleReroll();
            case 'buyTier': return handleTier();
            case 'endTurn': return hanldeEndTurn();
            case 'retireModal': return showModal('#retireModal');
            case 'retire': return handleRetire();
            case 'dismiss': return dismissModal();
        }
    });
});

function showModal(query){
    document.querySelector('#retireModal').style.display = 'block';
    _isModal = true;
}

function dismissModal(){ 
    document.querySelectorAll('.modal').forEach(e => e.style.display = 'none'); 
    _isModal = false;
}

/* ------------------------------------------------------
handlers
*/

async function handleRetire(){
    await fetchHandler('api/retire/');
    dismissModal();
    resetCombat();
}

async function hanldeEndTurn(){
    const data = await fetchHandler('api/endTurn/');
    onCombatEnter();
}

async function handleTier(){
    const data = await fetchHandler('api/buy_tier/');
}

async function handleBuy(element){
    const data = await fetchHandler('api/buy/', {
        id: parseInt(element.dataset.id),
        index: parseInt(element.dataset.index)
    });
}

async function handleReroll(){
    const data = await fetchHandler('api/reroll/');
}

/* ------------------------------------------------------
Fetch
*/

async function fetchHandler(url = '', data = {}, option = {}){
    const res = await fetchCSRF(url, data, option);

    if(res.status == 500){
        document.body.innerHTML = await res.text();
        return null;
    }
        
    const serverData = await res.json();

    if(res.status == 400){
        console.error(serverData);
        document.querySelector('#error').textContent = JSON.stringify(serverData);
        return null;
    }        

    console.log(url, "data:", data, "server:",serverData);
    updateAll(serverData);    
    return serverData;
}


function getToken(){ return document.cookie.match(/csrftoken=([^;]+)/)[1]; }

function fetchCSRF(url = '', data = {}, option = {}){
    return fetch(url, {
        method:"POST",
        ...option,        
        body: JSON.stringify(data),
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getToken()
        }
    });
}

/* ------------------------------------------------------
Update
*/
function updateAll(serverData){
    const {name, data, creature, enemy, state}  = serverData;
    document.querySelector('#game').dataset.state = state;
    document.querySelector('#game .title').textContent = state;

    updateCombat(creature, enemy);
    updateData(data);
    updateCreature(creature);
}

function updateCombat(user, enemy){
    updateElement(user, document.querySelector('#combat .user'));
    updateElement(enemy, document.querySelector('#combat .enemy'));
}

function updateData(serverData){
    const {store_list, ...data} = serverData;

    if(data.tier >= 6)
        document.querySelector('#tier-button').disabled = true;

    updateElement(data, document.querySelector('#data'));
    updateList(store_list, document.querySelector(`#data .list`), true)
}

function updateCreature(serverData){
    const {items, ...data} = serverData;

    updateElement(data, document.querySelector('#creature .data'));
    updateList(items, document.querySelector(`#creature [name=items]`));    
}

function updateList(list, parent, isBuy){
    parent.innerHTML = '';

    parent.append(...list.map((item, index) => getItemClone(item, isBuy, index)));    
}

function getItemClone(item, isBuy, index){
    const element = document.querySelector('template').content.cloneNode(true);
    updateElement(item, element);
    element.querySelectorAll('[data-id]').forEach(e => e.dataset.id = item.id);
    element.querySelectorAll('i').forEach(e => {
        e.setAttribute("class", item.type.icon);
        e.setAttribute("title", item.type.name);
    });

    if(item.count){
        element.querySelector('[name=count]').textContent = item.count
    }

    const button = element.querySelector('button');
    if(isBuy){
        button.dataset.id = item.id;
        button.dataset.index = index;
    }
    else{
        button.remove();
    }

    return element;
}


function updateElement(data, parent = document){
    const update = ([key,value]) => parent.querySelectorAll(`[name=${key}] `).forEach(element => element.textContent=value)

    if(parent && data)
        Object.entries(data).forEach(update);
}