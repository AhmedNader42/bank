function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const loginRoute = {
        method: "post",
        url: "http://localhost:8000/api/v1/dj-rest-auth/login/",
        data: {
            "username": String(username),
            "password": String(password)
        },
    };

    axios(loginRoute)
        .then((d) => {
            const token = d.data.key
            console.log(token);
            console.log(username);
            localStorage.setItem("token", token);
            localStorage.setItem("username", username);
            window.location.href = "Profile/profile.html";
        })
        .catch((e) => {
            alert("error loggin in.")
        });
    
}
