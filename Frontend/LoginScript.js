function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const loginRoute = {
        method: "post",
        url: "http://localhost:8000/api/v1/dj-rest-auth/login/",
        data: {
            username: String(username),
            password: String(password),
        },
    };

    axios(loginRoute)
        .then((d) => {
            const token = d.data.key;
            console.log(token);
            console.log(username);
            localStorage.setItem("token", token);
            localStorage.setItem("username", username);
            loadProfile(token, username);
        })
        .catch((e) => {
            alert("error loggin in.");
        });
}

function loadProfile(token, username) {
    const userProfile = {
        method: "get",
        url: `http://localhost:8000/users/${username}/`,
        headers: {
            Authorization: `Token ${token}`,
        },
    };

    axios(userProfile)
        .then((res) => {
            console.log(res);
            const userData = res.data;
            let user = {
                pk: userData["pk"],
                username: userData["username"],
                email: userData["email"],
                user_type: userData["user_type"],
            };
            localStorage.setItem("user", JSON.stringify(user));
            switch (user.user_type) {
                case 1:
                    window.location.href = "banker/banker.html";
                    break;
                case 2:
                    window.location.href = "customer/customer.html";
                    break;
                case 3:
                    window.location.href = "funder/funder.html";
                    break;
                default:
                    break;
            }
        })
        .catch((e) => {
            alert("Profile Error!");
            window.location.href = "Login.html";
        });
}
