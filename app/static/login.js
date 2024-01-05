var signIn_form =  document.getElementById("signIn_form");
var create_user =  document.getElementById("create_user");
var signInButton =  document.getElementById("signInButton");
var submit =  document.getElementById("submit");
var backToSignIn =  document.getElementById("backToSignIn");
var createAccount =  document.getElementById("createAccount");
var username =  document.getElementById("username");
var password =  document.getElementById("password");


signInButton.onclick = function () {
    /*
    signIn_form.style.left = "-450px"
    create_user.style.left = "40px"
    */
/*    if (username.value === "elyas.jabari" && password.value === "anmelden"){
        window.location.href = "../templates/support.html";
    } else if (username.value === "" && password.value === ""){
        alert("enter your username and password")
    }else {
        alert("Wrong password")
    }*/

    // send POST mit username/password as JSON

/*    const user_query = "SELECT * FROM tbl_user WHERE username = ?";
    console.log(user_query);
    if (user_query.valueOf() === username.valueOf()){
        console.log("anmelden")
    }else {
        console.log("etwas schief gelaufen")
    }*/

    fetch('http://127.0.0.1:5000/user/verify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username.value,
            password: password.value,
        }),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status === 200) {
                window.location.replace(data.account_url);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });


}

submit.onclick = function () {
    var usernameCreateUser = document.getElementById("usernameCreateUser");
    var passwordCreateUser = document.getElementById("passwordCreateUser");
    var confirmPassword = document.getElementById("confirmPassword");
    var role_id = document.querySelector('input[name="role_id"]:checked');

    if (passwordCreateUser.value !== confirmPassword.value) {
        alert("Passwörter stimmen nicht überein");
        return;
    }
    if (role_id === null) {
        alert("Bitte ein Rolle auswählen");
        return;
    }


    fetch('http://127.0.0.1:5000/user/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: usernameCreateUser.value,
            password: passwordCreateUser.value,
            role_id: role_id ? role_id.value : null,
        }),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status === 200) {
                console.log("daten ist angekomme: " + data)
                //window.location.replace(data.account_url);
            } else {
                console.log(data)
            }
        })
        .catch(error => {
            console.error('Fehler:', error);
        });
}


createAccount.onclick = function () {
    signIn_form.style.left = "-450px"
    create_user.style.left = "40px"
}
backToSignIn.onclick = function () {
    signIn_form.style.left = "40px"
    create_user.style.left = "450px"
}

/* var backToMain =  document.getElementById("backToMain");
backToMain.onclick = function () {
    window.location.href = "login.html";
} */


