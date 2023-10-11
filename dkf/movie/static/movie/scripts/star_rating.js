renderStars();



let isRated = false;
let rateField = document.getElementById('id_rating');
let rateParagraph = document.querySelector('.js-set-rate');

if (rateField.value) {
    colorRating();
}



let rate;

document.querySelectorAll('.js-rate-button').forEach((rateButton, index) => {
    rateButton.addEventListener('click', () => {
        isRated = !isRated;
    });
});

document.querySelectorAll('.js-rate-button').forEach((rateButton, index) => {
    rateButton.addEventListener('mouseover', () => {
        if (!isRated) {
            rate = (index + 2) * 5/10;
            for (let i = 0; i <= 16; i++) {
                let previousButton = document.querySelectorAll('.js-rate-button')[i];
                if (previousButton) {
                    changeImage(previousButton, i, index);
                }
            }
            rateParagraph.innerHTML = `Oceniasz na: ${rate} / 8.5`;
            if (rateField) {
                rateField.value = rate;
            }
        }
    });
});

function renderStars() { //generate 8.5 stars
    let starsHTML = '';
    starsHTML += '<div class="star"> <button type="button" class="rate-button js-rate-button"> <img src="/media/rates/gwiazdencja_transparent.png" class="star-image js-star-image"> </button>  </div>'
    for (let i = 0; i < 7; i++) {
        starsHTML += '<div class="star"> <button type="button" class="rate-button js-rate-button"> <img src="/media/rates/gwiazdencja_lewa_transparent.png" class="star-image js-star-image"> </button>  </div>\n' +
            '                        <div class="star"> <button type="button" class="rate-button js-rate-button"> <img src="/media/rates/gwiazdencja_prawa_transparent.png " class="star-image js-star-image"> </button> </div>'
    }
    starsHTML += '<div class="star"> <button type="button" class="rate-button js-rate-button"> <img src="/media/rates/gwiazdencja_lewa_transparent.png" class="star-image js-star-image"> </button>  </div>'
    document.querySelector('.js-voting-stars').innerHTML = starsHTML;
}

function colorRating() {
    isRated = true;
    let lastColoredStar = (rateField.value * 2) - 2;
    console.log(lastColoredStar);
    for (let i = 0; i <= 16; i++) {
        let previousButton = document.querySelectorAll('.js-rate-button')[i];
        if (previousButton) {
            changeImage(previousButton, i, lastColoredStar);
        }
    }
    rateParagraph.innerHTML = `Oceniasz na: ${rateField.value} / 8.5`;
}


function changeImage(starButton, currentIndex, maxColorIndex) {
    let img = starButton.querySelector('.js-star-image')
    let currentSrc = img.src;
    if (currentIndex <= maxColorIndex) {
        img.src = currentSrc.replace('transparent', 'color');
    } else {
        img.src = currentSrc.replace('color', 'transparent');
    }
}