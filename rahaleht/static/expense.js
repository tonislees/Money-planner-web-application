document.addEventListener('DOMContentLoaded', function() {
    function addOptions() {
        const subCatNames = JSON.parse(document.getElementById('subcategories-names-data').textContent);
        const subCat = JSON.parse(document.getElementById('subcategories-data').textContent);
        const catSelect = document.getElementById('categories');
        const subCatSelect = document.getElementById('subcategories');
        const selectedValue = catSelect.value;
        const options = subCat[selectedValue] || [];
        subCatSelect.innerHTML = '';
        for (let i=0; i<options.length; i++) {
            const option = document.createElement('option');
            option.value = options[i];
            option.textContent = subCatNames[selectedValue][i];
            subCatSelect.appendChild(option)
        }
    }

    function defaultMonth() {
        const monthSelect = document.getElementById('month-select')
        const monthSelect2 = document.getElementById('month-select-2')
        const theMonthSelect = monthSelect || monthSelect2
        const date = new Date()
        let month = date.getMonth();
        if (month >= 9) {
            month = (month + 1).toString()
        } else {
            month = '0' + (month + 1).toString()
        }
        theMonthSelect.value = month
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
            const catContainerBudget = document.getElementById(cat + '-head-budget');
            const pair = [catContainer]
            if (catContainerBudget) {
                const pair = [catContainer, catContainerBudget]
            }
            const subCategories = document.getElementById(cat + '-container');
            pair.forEach((element) => {
                element.addEventListener('click', () => {
                    const catIcon = document.getElementById(cat + '-icon')
                    const catSum = document.getElementById(cat)
                    const catSumBudget = document.getElementById(cat + '-budget')
    
                    catIcon.classList.toggle('cat-closed')
                    catSum.classList.toggle('cat-closed')
                    catSumBudget.classList.toggle('cat-closed')
    
                    const children = subCategories.children.length;
                    subCategories.style.maxHeight = children * 62.25 + 'px'
                    subCategories.classList.toggle('closed');
                    const currentCatDiv = document.getElementById(cat + '-div')
                    if (currentCatDiv.nextElementSibling.classList.contains('cat-container')) {
                        currentCatDiv.nextElementSibling.querySelectorAll('.cat-head').forEach((elem) => {
                            elem.classList.toggle('top-sibling')
                        })
                        
                        currentCatDiv.querySelectorAll('.cat-head').forEach((elem) => {
                            elem.classList.toggle('bottom-sibling')
                        })
                    }
                })
            })

        }
    }

    

    if (window.location.pathname.startsWith('/new-expense') || window.location.pathname.startsWith('/edit-expense')) {
        const catSelect = document.getElementById('categories');
        catSelect.addEventListener('change', () => {
            addOptions();
        });
        addOptions();
        defaultMonth();
    } else if (window.location.pathname === '/overview') {
        getMaxHeights()
        changeYearly();
        defaultMonth();
        closeCat()
    } else if (window.location.pathname === '/budgets') {
        defaultMonth();
    };
});