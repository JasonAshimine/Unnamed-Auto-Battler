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