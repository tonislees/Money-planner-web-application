document.addEventListener('DOMContentLoaded', function() {
    function addOptions() {
        const subCat = JSON.parse(document.getElementById('subcategories-data').textContent);
        const catSelect = document.getElementById('categories');
        const subcatSelect = document.getElementById('subcategories');
        const selectedValue = catSelect.value;
        const options = subCat[selectedValue] || [];
        subcatSelect.innerHTML = '';
        options.forEach((subcategory) => {
            const option = document.createElement('option');
            option.value = subcategory;
            option.textContent = subcategory;
            subcatSelect.appendChild(option)
        });
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
        const yearlyLabel = document.getElementById('yearly-button-label')
        const monthSelect = document.getElementById('month-select')
        document.getElementById('yearly-button').addEventListener('change', function() {
            if (this.checked) {
                yearlyLabel.innerText = 'Yearly'
                monthSelect.classList.add('yearly-button')
            }
            else {
                yearlyLabel.innerText = 'Monthly'
                monthSelect.classList.remove('yearly-button')
            }
        })
    }

    if (window.location.pathname === '/new-expense') {
        catSelect.addEventListener('change', () => {
            addOptions();     
        });
        addYears();
    } else if (window.location.pathname === '/overview') {
        addYears();
        changeYearly();
    };
});