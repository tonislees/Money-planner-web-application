document.addEventListener('DOMContentLoaded', function() {
    function addZeros() {
        const fields = document.querySelectorAll('.budget-form');
        fields.forEach(function(field) {
            if (field.value.trim() === '') {
                field.value = '0.00'
            } else {
                field.value = parseFloat(field.value).toFixed(2);
            }
        })
    }

    function onChangeAddZeros() {
        const fields = document.querySelectorAll('.budget-form');
        fields.forEach(function(field) {
            field.addEventListener('blur', () => {
                addZeros();
                localStorage.setItem(field.id, field.value);
            })
            field.addEventListener('click', () => {
                field.value = ""
            })
        })
    }

    function loadFieldValues() {
        const fields = document.querySelectorAll('.budget-form');
        fields.forEach(function(field) {
            const value = localStorage.getItem(field.id);
            if (value) {
                field.value = value;
            }
        })
        const nameField = document.getElementById('name');
        const name = localStorage.getItem('name');
        if (name) {
            nameField.value = name;
            nameField.classList.add('form-text');
        }

        const defaultValue = document.getElementById('default-budget-button')
        const savedValue = localStorage.getItem('default')
        if (savedValue == '1') {
            defaultValue.checked = true
        }
    }

    function addTotals() {
        const cats = JSON.parse(document.getElementById('categories-data').textContent)
        const subCats = JSON.parse(document.getElementById('subcategories-data').textContent)

        const totalIncomesElement = document.getElementById('total-incomes')
        const totalExpensesElement = document.getElementById('total-expenses')
        const balanceElement = document.getElementById('balance')

        let totalIncomes = 0;
        let totalExpenses = 0;
        let balance = 0;

        for(let cat of cats) {
            const catTotalElement = document.getElementById(cat.replace('_', '-') + '-total')
            let catTotal = 0;
            for(let subCat of subCats[cat]) {
                const subCatField = document.getElementById(subCat);
                catTotal += parseFloat(subCatField.value)
            }
            if (cat === 'incomes') {
                totalIncomes += catTotal
            } else {
                totalExpenses += catTotal
            }
            catTotalElement.textContent = parseFloat(catTotal).toFixed(2).toLocaleString() + ' €'
        }

        balance = totalIncomes - totalExpenses;

        totalIncomesElement.textContent = parseFloat(totalIncomes).toFixed(2).toLocaleString() + ' €';
        totalExpensesElement.textContent = parseFloat(totalExpenses).toFixed(2).toLocaleString() + ' €';
        balanceElement.textContent = parseFloat(balance).toFixed(2).toLocaleString() + ' €';
    }

    function onChangeAddTotals() {
        const fields = document.querySelectorAll('.budget-form');
        fields.forEach(function(field) {
            field.addEventListener('change', () => {
                addTotals()
            })
        })
    }

    function changeNameInput() {
        const nameField = document.getElementById('name');
        nameField.addEventListener('click', () => {
            nameField.value = ""
            nameField.classList.add('form-text')
        })

        nameField.addEventListener('blur', () => {
            if (nameField.value.trim() !== '') {
                localStorage.setItem('name', nameField.value);
            } else {
                localStorage.removeItem('name');
            }
        })
    }

    function preventEnterSubmit() {
        const form = document.getElementById('budget-form');
        form.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
            }
        });
    }

    function resetDefaultBudget() {
        const resetButton = document.getElementById('reset-default-button');

        resetButton.addEventListener('click', () => {
            const fields = document.querySelectorAll('.budget-form');
            fields.forEach(function(field) {
                field.value = '0.00';
                localStorage.setItem(field.id, field.value);
            })
            addTotals();
        });
    }

    function afterSaveClearLocalStorage() {
        document.getElementById('save').addEventListener('click', () => {
            localStorage.clear();
        });
    }

    async function fetchBudgetData(year, month) {
        const currentUserId = document.getElementById('current-user-id').value;
        const response = await fetch(`/api/budgetdata/${currentUserId}/${parseInt(month)}/${parseInt(year)}`);
        const data = await response.json();
        return data;
    }

    async function addBudgetNumbers(newBudgetUrlBase, editBudgetUrlBase) {
        const yearElement = document.getElementById('year-select');
        const monthElement = document.getElementById('month-select');
        const addBudget = document.getElementById('add-budget')
        const defaultName = document.getElementById('budget-default-name')
        const nameIcon = document.getElementById('budget-edit')
        const editElement = document.getElementById('edit-link')
        const editNewBudget = document.getElementById('budget-default-name')
        const incomesTotalText = document.getElementById('total-incomes')
        const expensesTotalText = document.getElementById('total-expenses')
        const budgetLegendText = document.getElementById('budget-legend')
        const budgetDefaultText = document.getElementById('budget-default').value
        const budgetLegendDefaultText = document.getElementById('budget-legend-default')

        const data = await fetchBudgetData(yearElement.value, monthElement.value);
        if (!data['data']['0']) {
            data['data']['0'] = {'incomes': 0,
                                'living_costs': 0,
                                'personal_expenses': 0,
                                'investing': 0}
            addBudget.classList.remove('name-close')
            nameIcon.classList.add('name-close')
            defaultName.classList.remove('name-close')
            budgetLegendDefaultText.classList.remove('name-close')
            budgetLegendText.classList.add('name-close')
            editNewBudget.setAttribute('href', `${newBudgetUrlBase}${yearElement.value}/${monthElement.value}`)
        } else {
            nameIcon.classList.remove('name-close')
            addBudget.classList.add('name-close')
            defaultName.classList.add('name-close')
            budgetLegendDefaultText.classList.add('name-close')
            budgetLegendText.classList.remove('name-close')
            editElement.setAttribute('href', `${editBudgetUrlBase}${data['data']['0'].id}`)
            const incomes = data['data']['0'].incomes
            const expenses = data['data']['0'].living_costs + data['data']['0'].personal_expenses + data['data']['0'].investing
            incomesTotalText.textContent = incomes.toFixed(2).toLocaleString() + ' €'
            expensesTotalText.textContent = expenses.toFixed(2).toLocaleString() + ' €'
            console.log(data['data']['0'])
            if (data['data']['0'].is_default) {
                budgetLegendText.textContent = data['data']['0'].name + budgetDefaultText
            } else {
                budgetLegendText.textContent = data['data']['0'].name
            }
            
        }

        const incomesTotalField = document.getElementById('incomes-total');
        const personalExpensesTotalField = document.getElementById('personal-expenses-total');
        const livingCostsTotalField = document.getElementById('living-costs-total');
        const investingTotalField = document.getElementById('investing-total');
        
        incomesTotalField.textContent = parseFloat(data['data']['0'].incomes).toFixed(2) + ' €'
        personalExpensesTotalField.textContent = parseFloat(data['data']['0'].personal_expenses).toFixed(2) + ' €'
        livingCostsTotalField.textContent = parseFloat(data['data']['0'].living_costs).toFixed(2) + ' €'
        investingTotalField.textContent = parseFloat(data['data']['0'].investing).toFixed(2) + ' €'
    }

    async function onChangeAddNumbers(editNewBudgetUrl, editBudgetUrlBase) {
        const yearElement = document.getElementById('year-select');
        const monthElement = document.getElementById('month-select');

        yearElement.addEventListener('change', async () => {
            addBudgetNumbers(editNewBudgetUrl, editBudgetUrlBase);
        })
        monthElement.addEventListener('change', async () => {
            addBudgetNumbers(editNewBudgetUrl, editBudgetUrlBase);
        })
    }

    function checkCheckbox() {
        const button = document.getElementById('default-budget-button');
        const buttonLabel = document.getElementById('default-budget-button-label');
        const defaultButtonLang = document.getElementById('default-budget-button-lang');
        const removeDefaultButtonLang = document.getElementById('remove-default-budget-button-lang');
        if (button.checked) {
            buttonLabel.innerText = removeDefaultButtonLang.value
            localStorage.setItem('default', 1)
        }
        else {
            buttonLabel.innerText = defaultButtonLang.value
            localStorage.setItem('default', 0)
        }
    }

    function changeDefaultBudgetButton() {
        const button = document.getElementById('default-budget-button');

        button.addEventListener('change', function() {
            checkCheckbox();
        })
    }

    if (window.location.pathname.startsWith('/new-budget') || window.location.pathname.startsWith('/edit-budget')) {
        loadFieldValues();
        addZeros();
        onChangeAddZeros();
        addTotals();
        onChangeAddTotals();
        changeNameInput();
        preventEnterSubmit();
        resetDefaultBudget();
        checkCheckbox();
        changeDefaultBudgetButton();
        afterSaveClearLocalStorage();
        window.addEventListener('beforeunload', () => {
            localStorage.removeItem('default');
        })
    } else if (window.location.pathname === '/budgets') {
        const NewBudgetUrl = document.getElementById('budget-default-name').getAttribute('href')
        const editBudgetUrl = document.getElementById('edit-link').getAttribute('href')
        addBudgetNumbers(NewBudgetUrl, editBudgetUrl);
        onChangeAddNumbers(NewBudgetUrl, editBudgetUrl);
    }
});

