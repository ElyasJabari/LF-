var form1 =  document.getElementById("form1");
var form2 =  document.getElementById("form2");
var next1 =  document.getElementById("next1");
var submit =  document.getElementById("submit");
var back1 =  document.getElementById("back1");
var createAccount =  document.getElementById("createAccount");
var username =  document.getElementById("username");
var password =  document.getElementById("password");

next1.onclick = function () {
    /*
    form1.style.left = "-450px"
    form2.style.left = "40px"
    */
    if (username.value === "elyas.jabari" && password.value === "anmelden"){
        window.location.href = "../templates/ticketlist.html";
    } else if (username.value === "" && password.value === ""){
        alert("enter your username and password")
    }else {
        alert("Wrong password")
    }
}
createAccount.onclick = function () {
    form1.style.left = "-450px"
    form2.style.left = "40px"
}
back1.onclick = function () {
    form1.style.left = "40px"
    form2.style.left = "450px"
}
submit.onclick = function () {
    window.location.href = "test.html";
}

/* var backToMain =  document.getElementById("backToMain");
backToMain.onclick = function () {
    window.location.href = "login.html";
} */


