document.addEventListener('DOMContentLoaded', function() {
    function addOptions() {
        const subCat = JSON.parse(document.getElementById('subcategories-data').textContent);
        const catSelect = document.getElementById('categories');
        const subCatSelect = document.getElementById('subcategories');
        const selectedValue = catSelect.value;
        const options = subCat[selectedValue] || [];
        subCatSelect.innerHTML = '';
        options.forEach((subcategory) => {
            const option = document.createElement('option');
            option.value = subcategory;
            option.textContent = subcategory;
            subCatSelect.appendChild(option)
        });
    }

    function defaultMonth() {
        const monthSelect = document.getElementById('month-select')
        const date = new Date()
        let month = date.getMonth();
        if (month >= 9) {
            month = (month + 1).toString()
        } else {
            month = '0' + (month + 1).toString()
        }
        monthSelect.value = month
    }

    function addYears() {
        const yearSelect = document.getElementById('year-select');
        const date = new Date();
        const year = date.getFullYear();
        for (let i=year; i>=2015; i--) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            yearSelect.appendChild(option);
        }
    }

    function changeYearly() {
        const yearlyLabel = document.getElementById('yearly-button-label');
        const monthSelect = document.getElementById('month-select');

        const yearlyYearLang = document.getElementById('yearly-year-lang');
        const yearlyMonthLang = document.getElementById('yearly-month-lang');

        document.getElementById('yearly-button').addEventListener('change', function() {
            if (this.checked) {
                yearlyLabel.innerText = yearlyYearLang.value;
                monthSelect.classList.add('yearly-button');
            }
            else {
                yearlyLabel.innerText = yearlyMonthLang.value
                monthSelect.classList.remove('yearly-button');
            }
        })
    }

    function getMaxHeights() {
        const categories = JSON.parse(document.getElementById('categories-data').textContent);
        for(let cat of categories) {
            const subCategories = document.getElementById(cat + '-container');
            const children = subCategories.children.length;
            subCategories.style.maxHeight = children * 62.25 + 'px'
        }
    }

    function closeCat() {
        const categories = JSON.parse(document.getElementById('categories-data').textContent);
        for(let cat of categories) {
            const catContainer = document.getElementById(cat + '-head');
            const subCategories = document.getElementById(cat + '-container');
            catContainer.addEventListener('click', () => {
                const catIcon = document.getElementById(cat + '-icon')
                const catSum = document.getElementById(cat)

                catIcon.classList.toggle('cat-closed')
                catSum.classList.toggle('cat-closed')

                const children = subCategories.children.length;
                subCategories.style.maxHeight = children * 62.25 + 'px'
                subCategories.classList.toggle('closed');
                const currentCatDiv = document.getElementById(cat + '-div')
                if (currentCatDiv.nextElementSibling.classList.contains('cat-container')) {
                    currentCatDiv.nextElementSibling.querySelector('.cat-head').classList.toggle('top-sibling')
                    currentCatDiv.querySelector('.cat-head').classList.toggle('bottom-sibling')
                }
            })
        }
    }

    if (window.location.pathname === '/new-expense' || window.location.pathname.startsWith('/edit-expense')) {
        const catSelect = document.getElementById('categories');
        catSelect.addEventListener('change', () => {
            addOptions();     
        });
        addOptions();
    } else if (window.location.pathname === '/overview') {
        getMaxHeights()
        addYears();
        changeYearly();
        defaultMonth();
        closeCat()
    };
});