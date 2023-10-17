let areFiltersVisible = false;
let filters = document.querySelector(".js-filters");
filters.style.display = "none";
// let filtersForm = document.getElementById('js-filters');
console.log(searchedMovies);

let input =  document.querySelector('.search-input');
input.value = searchedMovies;

let showFiltersButton = document.querySelector('.js-show-filters-button')


showFiltersButton
    .addEventListener('click', () => {
        areFiltersVisible = !areFiltersVisible;
        if (areFiltersVisible) {
            // filtersForm.classList.remove('hidden-filters');
            // filtersForm.classList.add('visible-filters');
            filters.style.display = "flex";
            showFiltersButton.innerHTML = 'Schowaj filtry';
        } else {
            // filtersForm.classList.remove('visible-filters');
            // filtersForm.classList.add('hidden-filters');
            filters.style.display = "none";
            showFiltersButton.innerHTML = 'Pokaż filtry';
        }
        // if (areFiltersVisible) {
        //     filters.style.display = "flex";
        //     showFiltersButton.innerHTML = 'Schowaj filtry';
        // }
        // else {
        //     filters.style.display = "none";
        //     showFiltersButton.innerHTML = 'Pokaż filtry';
        // }
    })
