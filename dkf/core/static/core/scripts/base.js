let menuVisible = false;

// let menu = document.getElementsByClassName(".js-account-menu")
let menu = document.querySelector(".account-menu");
menu.style.transform='scaleY(0)';
let toggleButton = document.querySelector('.js-toggle-button');


console.log('hej');
toggleButton.addEventListener('click', () => {
    menuVisible = !menuVisible;
    if (menuVisible) {
        menu.style.transform='scaleY(1)';
    } else {
        menu.style.transform='scaleY(0)';
    }
})