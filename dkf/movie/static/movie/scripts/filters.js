let areFiltersVisible = false;
let filters = document.querySelector(".js-filters");

filters.style.transform = 'scale(0)';
console.log(searchedMovies);

let input =  document.querySelector('.search-input');
input.value = searchedMovies;

let showFiltersButton = document.querySelector('.js-show-filters-button')


showFiltersButton
    .addEventListener('click', () => {
        areFiltersVisible = !areFiltersVisible;
        if (areFiltersVisible) {
            filters.style.transform = 'scale(1)';
            showFiltersButton.innerHTML = 'Schowaj filtry';
        } else {
            filters.style.transform = 'scale(0)';
            showFiltersButton.innerHTML = 'Pokaż filtry';
        }
    })
