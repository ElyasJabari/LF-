const date = new Date();

let day = date.getDate()
let month = date.getMonth()+1
let year = date.getFullYear()

let currentDate = `${day}.${month}.${year}`

let currentDateInput = document.getElementById("creationD")
currentDateInput.addEventListener('click', getCurrentDate)
function getCurrentDate() {
    currentDateInput.value = currentDate
}

