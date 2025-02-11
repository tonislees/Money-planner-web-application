document.addEventListener('DOMContentLoaded', function() {
    function sum(dict) {
        const array = Object.keys(dict)
        const intArray = array.map(Number)
        console.log(intArray)
        let s = intArray.reduce((accumulator, currentValue) => accumulator + currentValue, 0)
        return s
    }

    function sortData(data) {
        let allData = {}

        data['data'].forEach(element => {
            if (!(element['category'] in allData)) {
                allData[element['category']] = {};
            }
            if (!(element['subcategory'] in allData[element['category']])) {
                allData[element['category']][element['subcategory']] = {};
            }
            const date = new Date()
            const formatedDate = `${date.getMonth()}.${date.getDate()} ${date.getHours()}:${date.getMinutes()}`
            allData[element['category']][element['subcategory']][element['money']] = [element.description, element.expense_id, element.date]
        });
        return allData
    }

    async function fetchData(yearly, year, month) {
        const currentUserId = document.getElementById('current-user-id').value
        const response = await fetch(`/api/userdata/${currentUserId}/${yearly}/${month}/${year}`)
        const data = await response.json()
        return data
    }

    async function addNumbers(yearly, year, month) {
        const fetchedData = await fetchData(yearly, year, month)
        const allSubCat = JSON.parse(document.getElementById('subcategories-data').textContent);
        data = sortData(fetchedData)

        let totalIn = 0
        let totalOut = 0
        for(let cat in allSubCat) {
            let value = allSubCat[cat]
            let catNr = 0
            const catHTML = document.getElementById(cat)
            const catTotal = document.getElementById(cat + '-total')
            for(let subCat of value) {
                const subCatHTML = document.getElementById(subCat)
                if (data.hasOwnProperty(cat) && data[cat].hasOwnProperty(subCat)) {
                    let nrArray = data[cat][subCat]
                    subCatHTML.textContent = parseFloat(sum(nrArray)).toLocaleString() + ' €'
                    catNr += sum(nrArray)
                } else {
                    subCatHTML.textContent = '0 €'
                }
            }
            catHTML.textContent = parseFloat(catNr).toLocaleString() + ' €';
            catTotal.textContent = parseFloat(catNr).toLocaleString() + ' €';
            if (cat === 'incomes') {
                totalIn += catNr
            } else {
                totalOut += catNr
            }
        }

        const totalExp = document.getElementById('total-expenses');
        const money = document.getElementById('money-left');

        totalExp.textContent = parseFloat(totalOut).toLocaleString() + ' €';
        money.textContent = parseFloat(totalIn - totalOut).toLocaleString() + ' €';
    }

    function passParams(yearly, year, month) {
        const links = document.querySelectorAll('a[id$="-icon"]');
        links.forEach(link => {
            const url = new URL(link.href);
            const category = link.id.split('-')[0]
            url.searchParams.set('category', category)
            url.searchParams.set('yearly', yearly)
            url.searchParams.set('year', year);
            url.searchParams.set('month', month);
            link.href = url.toString();
        })
    }

    function getMaxHeightsSub(cat) {
        const categories = JSON.parse(document.getElementById('subcategories-data').textContent);
        for(let subCat of categories[cat]) {
            const expenses = document.getElementById(subCat + '-expenses');
            const children = expenses.children.length;
            expenses.style.maxHeight = children * 62.25 + 'px'
        }
    }

    async function addCatNumbers(yearly, year, month, cat) {
        const fetchedData = await fetchData(yearly, year, month)
        const allSubCat = JSON.parse(document.getElementById('subcategories-data').textContent);
        data = sortData(fetchedData)

        let total = 0
        const catTotal = document.getElementById('total-expenses');
        const editUrl = document.getElementById('data-url').dataset.editUrl;
        const currentUrl = window.location.pathname + window.location.search;
        for(let subCat of allSubCat[cat]) {
            let subCatTotalValue = 0
            if (data.hasOwnProperty(cat) && data[cat].hasOwnProperty(subCat)) {
                const expenseDict = data[cat][subCat]
                const expensesDiv = document.getElementById(subCat + '-expenses')
                const defaultChild = expensesDiv.querySelector('.subcat-expense-default')
                console.log(expensesDiv)
                console.log(defaultChild)
                const subCatTotal = document.getElementById(subCat)
                if (expensesDiv.querySelector('.subcat-expense-default')) {
                    console.log('removed')
                    expensesDiv.removeChild(defaultChild)
                }
                total += sum(expenseDict)
                for(const [expense, expenseData] of Object.entries(expenseDict)) {
                    subCatTotalValue += parseFloat(expense, 10)

                    const newExpense = document.createElement('div')
                    newExpense.classList.add('subcat-name')

                    const expenseDescDiv = document.createElement('div')
                    expenseDescDiv.classList.add('desc-div')
                    const expenseDescription = document.createElement('p')
                    expenseDescDiv.appendChild(expenseDescription)
                    expenseDescription.classList.add('text')
                    expenseDescription.classList.add('text-s')
                    expenseDescription.classList.add('account-form-text')
                    expenseDescription.setAttribute('id', expenseData[0] + '-description')
                    expenseDescription.textContent = expenseData[0] + ' - ' + expenseData[2]
                    newExpense.appendChild(expenseDescDiv)
                    
                    const expenseSumDiv = document.createElement('div')
                    expenseSumDiv.classList.add('expense-sum-div')
                    const editExpenseIcon = document.createElement('a')
                    editExpenseIcon.classList.add('text')
                    editExpenseIcon.classList.add('text-s')
                    editExpenseIcon.classList.add('account-form-text')
                    editExpenseIcon.setAttribute('href', `${editUrl}${expenseData[1]}?next=${encodeURIComponent(currentUrl)}`)
                    const editIconSpan = document.createElement('span')
                    editIconSpan.classList.add('glyphicon')
                    editIconSpan.classList.add('glyphicon-pencil')
                    editExpenseIcon.appendChild(editIconSpan)
                    editExpenseIcon.style.display = 'none'
                    expenseSumDiv.appendChild(editExpenseIcon)

                    const expenseValue = document.createElement('p')
                    expenseValue.classList.add('text')
                    expenseValue.classList.add('text-s')
                    expenseValue.classList.add('account-form-text')
                    expenseValue.classList.add('expense-sum')
                    expenseValue.setAttribute('id', expenseData[1] + '-description')
                    expenseValue.textContent = parseFloat(expense).toLocaleString() + ' €'
                    expenseSumDiv.appendChild(expenseValue)
                    newExpense.appendChild(expenseSumDiv)

                    expensesDiv.appendChild(newExpense)
                }
                subCatTotal.textContent = parseFloat(subCatTotalValue).toLocaleString() + ' €';
            } 
        }

        getMaxHeightsSub(cat)
        checkHover()
        catTotal.textContent = parseFloat(total).toLocaleString() + ' €'
    }

    function closeSubCat(cat) {
        const categories = JSON.parse(document.getElementById('subcategories-data').textContent);
        for(let subCat of categories[cat]) {
            const catContainer = document.getElementById(subCat + '-head');
            const expense = document.getElementById(subCat + '-expenses');
            catContainer.addEventListener('click', () => {
                const children = expense.children.length;
                expense.style.maxHeight = children * 62.25 + 'px'
                expense.classList.toggle('closed');
                const currentSubCatDiv = document.getElementById(subCat + '-container')
                if (currentSubCatDiv.nextElementSibling && currentSubCatDiv.nextElementSibling.classList.contains('subcat-container')) {
                    currentSubCatDiv.nextElementSibling.querySelector('.cat-head').classList.toggle('top-sibling')
                    currentSubCatDiv.querySelector('.cat-head').classList.toggle('bottom-sibling')
                }
            })
        }
    }

    function addCorners(cat) {
        const categories = JSON.parse(document.getElementById('subcategories-data').textContent);
        for(let subCat of categories[cat]) {
            const currentSubCatDiv = document.getElementById(subCat + '-container')
            if (currentSubCatDiv.nextElementSibling && currentSubCatDiv.nextElementSibling.classList.contains('subcat-container')) {
                currentSubCatDiv.nextElementSibling.querySelector('.cat-head').classList.toggle('top-sibling')
                currentSubCatDiv.querySelector('.cat-head').classList.toggle('bottom-sibling')
            }
        }
    }

    function checkHover() {
        expensesDivs = document.querySelectorAll('div.subcat-name')
        console.log(expensesDivs)
        expensesDivs.forEach(element => {
            element.addEventListener('mouseover', () => {
                const anchor = element.querySelector('a');
                const money = element.querySelector('p.expense-sum')
                if (anchor) {
                    anchor.style.display = 'block';
                    money.style.display = 'none'
                }
            });
            element.addEventListener('mouseout', () => {
                const anchor = element.querySelector('a');
                const money = element.querySelector('p.expense-sum')
                if (anchor) {
                    anchor.style.display = 'none';
                    money.style.display = 'block'
                }
            });
        });
    }

    if (window.location.pathname === '/overview') {
        console.log(document.querySelectorAll('a[id$="-icon"]')[0].id)
        const yearlyValue = document.getElementById('yearly-button').checked
        const yearValue = document.getElementById('year-select').value
        const monthValue = document.getElementById('month-select').value
        addNumbers(yearlyValue, yearValue, monthValue)
        passParams(yearlyValue, yearValue, monthValue)

        document.getElementById('yearly-button').addEventListener('change', function() {
            const yearValue = document.getElementById('year-select').value
            const monthValue = document.getElementById('month-select').value
            addNumbers(this.checked, yearValue, monthValue)
            passParams(this.checked, yearValue, monthValue)
        })
        document.getElementById('month-select').addEventListener('change', function() {
            const yearlyValue = document.getElementById('yearly-button').checked
            const yearValue = document.getElementById('year-select').value
            addNumbers(yearlyValue, yearValue, this.value)
            passParams(yearlyValue, yearValue, this.value)
        })
        document.getElementById('year-select').addEventListener('change', function() {
            const yearlyValue = document.getElementById('yearly-button').checked
            const monthValue = document.getElementById('month-select').value
            addNumbers(yearlyValue, this.value, monthValue)
            passParams(yearlyValue, this.value, monthValue)
        })
    } else if (window.location.pathname.startsWith('/edit-category')) {
        const legend = document.querySelector('.cat-legend')
        const cat = legend.id.split('-')[0]
        const yearly = legend.id.split('-')[1]
        const year = legend.id.split('-')[2]
        const month = legend.id.split('-')[3]

        addCatNumbers(yearly, year, month, cat)
        closeSubCat(cat);
    }
})