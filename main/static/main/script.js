document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener('click', event => {
        if(event.target.id == "error")
            return event.target.textContent = '';

        if(event.target.nodeName !== 'BUTTON')
            return;

        switch(event.target.name){
            case 'buy': return handleBuy(event.target);
            case 'reroll': return handleReroll();
            case 'buyTier': return handleTier();
            case 'endTurn': return hanldeEndTurn();
        }
    });
});



/* ------------------------------------------------------
handlers
*/

async function hanldeEndTurn(){
    const data = await fetchHandler('api/endTurn/');
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

    updateAll(serverData);
    console.log(url, "data:", data, "server:",serverData);
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
    const {name, data, creature}  = serverData;

    updateData(data);
    updateCreature(creature);
}

function updateData(serverData){
    const {store_list, ...data} = serverData;

    updateElement(data, document.querySelector('#data .data'));
    updateList(store_list, document.querySelector(`#data .list`), true)
}

function updateCreature(serverData){
    const {items, ...data} = serverData;

    updateElement(data, document.querySelector('#creature .data'));
    

    //updateList(items, document.querySelector(`#creature [name=items]`))
    parent = document.querySelector("#creature .list");
    children = [...parent.children]

    items.forEach((item, index) => {
        node = children[index];
        if(node.dataset.id == item.id){
            let element = node.querySelector('[name=count]');
            let count = element.textContent;
            element.textContent = item.count;            
        }
        else{
            element = getItemClone(item);
            node.before(element);
            element.classList.add('glow');
        }
    });
}

function updateList(list, parent, isBuy){
    parent.innerHTML = '';

    parent.append(...list.map((item, index) => getItemClone(item, isBuy, index)));    
}

function getItemClone(data, isBuy, index){
    const element = document.querySelector('template').content.cloneNode(true);
    updateElement(data, element);
    element.querySelectorAll('[data-id]').forEach(e => e.dataset.id = data.id);

    const button = element.querySelector('button');
    if(isBuy){
        button.dataset.id = data.id;
        button.dataset.index = index;
    }
    else{
        button.remove();
    }

    return element;
}


function updateElement(data, parent = document){
    const update = ([key,value]) => parent.querySelectorAll(`[name=${key}] `).forEach(element => element.textContent=value)

    Object.entries(data).forEach(update);
}