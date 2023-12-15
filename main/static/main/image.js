document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".sprite").forEach(element => {
        element.addEventListener('animationend', () => {
            element.setAttribute('class', `sprite ${element.dataset.tag}-idle`);
        });
        element.onclick = () => handleImageClick(element);

    })
});

let toggle = false;

function handleImageClick(element){
    type = toggle ? 'attack' : 'death';
    toggle = !toggle;
    element.setAttribute('class', `sprite ${element.dataset.tag}-${type}`);
    console.log(type, element.dataset.tag)
}


async function test(index){
    const res = await fetchCSRF('api/player/');
    const data = await res.json();

    console.log(data);

    animateCombatRound(data, index)
}


function animateCombatRound(data, index){
    const {combat_log, enemy, creature} = data;

    const round = combat_log[index];

    const hp_bar = document.querySelector('#combat .user .progress-bar');
    const sprite = document.querySelector('#combat .user .progress-bar');

}

