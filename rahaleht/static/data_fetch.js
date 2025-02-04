document.addEventListener('DOMContentLoaded', function() {
    function sum(array) {
        let s = array.reduce((accumulator, currentValue) => accumulator + currentValue, 0)
        return s
    }

    function sortData(data) {
        let allData = {}

        data['data'].forEach(element => {
            if (!(element['category'] in allData)) {
                allData[element['category']] = {};
            }
            if (!(element['subcategory'] in allData[element['category']])) {
                allData[element['category']][element['subcategory']] = [];
            }
            allData[element['category']][element['subcategory']].push(element.money)
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
        data = sortData(fetchedData)
        for(let cat in data) {
            let value = data[cat]
            let catNrValue = 0
            const catHTML = document.getElementById(cat)
            for(let subcat in value) {
                let nrArray = value[subcat]
                const subcatHTML = document.getElementById(subcat)
                subcatHTML.value = sum(nrArray)
                catNrValue += sum(nrArray)
            }
            catHTML.value = catNrValue
        }
    }

    if (window.location.pathname === '/overview') {
        document.getElementById('yearly-button').addEventListener('change', function() {
            const yearValue = document.getElementById('year-select').value
            const monthValue = document.getElementById('month-select').value
            addNumbers(this.checked, yearValue, monthValue)
        })
        document.getElementById('month-select').addEventListener('change', function() {
            const yearlyValue = document.getElementById('yearly-button').value
            const yearValue = document.getElementById('year-select').value
            addNumbers(yearlyValue, yearValue, this.value)
        })
        document.getElementById('year-select').addEventListener('change', function() {
            const yearlyValue = document.getElementById('yearly-button').value
            const monthValue = document.getElementById('month-select').value
            addNumbers(yearlyValue, this.value, monthValue)
        })
        const yearlyValue = document.getElementById('yearly-button').checked
        const yearValue = document.getElementById('year-select').value
        const monthValue = document.getElementById('month-select').value
        console.log(yearValue, monthValue)
        addNumbers(yearlyValue, yearValue, monthValue)
    }
})