function loadProfile() {
    const tokenData = loadToken();
    let token = tokenData["token"];
    let username = tokenData["username"];

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
                id: userData["id"],
                username: userData["username"],
                email: userData["email"],
                user_type: userData["user_type"],
            };
            localStorage.setItem("user", JSON.stringify(user));
            loadUserLoans();
        })
        .catch((e) => {
            alert("Profile Error!");
            window.location.href = "../Login.html";
        });
}
loadProfile();

function loadUserLoans() {
    const user = JSON.parse(localStorage.getItem("user"));
    const token = loadToken()["token"];
    const customerLoans = {
        method: "get",
        url: `http://localhost:8000/customer/${user.id}/`,
        headers: {
            Authorization: `Token ${token}`,
        },
    };

    axios(customerLoans)
        .then((res) => {
            console.log(res);
            listLoans(res.data);
        })
        .catch((e) => {
            alert("Error loading loans!");
        });
}

function listLoans(loans) {
    const table = document.getElementById("loansTable");
    let thead = table.createTHead();
    let tbody = table.createTBody();

    const LOAN_STATUS = {
        1: "PENDING",
        2: "APPROVED",
        3: "DENIED",
    };
    table.innerHTML = "";

    let th = thead.insertRow(0);
    th.insertCell(0).innerHTML = "Amount";
    th.insertCell(1).innerHTML = "Duration";
    th.insertCell(2).innerHTML = "Started";
    th.insertCell(3).innerHTML = "Status";

    for (let i = 0; i < loans.length; i++) {
        const loan = loans[i];
        let row = tbody.insertRow(i);

        row.insertCell(0).innerHTML = loan["amount"];
        row.insertCell(1).innerHTML = loan["duration"];
        row.insertCell(2).innerHTML = loan["started"];

        row.insertCell(3).innerHTML = LOAN_STATUS[loan["status"]];
    }

    table.appendChild(thead);
    table.appendChild(tbody);
}

function logout() {
    localStorage.clear();
    window.location.href = "../Login.html";
}

function loadToken() {
    let token = "";
    let username = "";
    try {
        token = localStorage.getItem("token").toString();
        username = localStorage.getItem("username").toString();
        return {
            token: token,
            username: username,
        };
    } catch (error) {
        window.location.href = "../Login.html";
    }
}
