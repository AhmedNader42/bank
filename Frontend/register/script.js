function register() {
    let validBodyInput = getBodyContent();
    const registerRequest = {
        method: "post",
        url: "http://localhost:8000/api/v1/dj-rest-auth/registration/",
        data: validBodyInput,
    };

    axios(registerRequest)
        .then((d) => {
            console.log(d);
            window.location.href = "../Login.html";
        })
        .catch((e) => {
            console.log(e.response);
            if (e.response) {
                console.log(e.response.data);
                const data = e.response.data;
                const keys = Object.keys(data);

                keys.forEach((key, index) => {
                    alert(data[key]);
                });
            }
        });
}

function getBodyContent() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const passwordConfirmation = document.getElementById("confirm-password").value;
    const user_type = document.getElementById("user-type").value;

    console.log(username);
    console.log(email);
    console.log(password);
    console.log(passwordConfirmation);
    console.log(user_type);

    if (password != passwordConfirmation) {
        alert("Passwords do not match");
    }

    return {
        username: String(username),
        email: String(email),
        password1: String(password),
        password2: String(passwordConfirmation),
        user_type: Number(user_type),
    };
}
