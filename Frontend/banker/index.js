"use strict";
let pendingLoans = [];
let pendingFunds = [];
let availableLoanOptions = [];
let availableFundOptions = [];

loadToken();
loadOptions("loan");
loadOptions("fund");
refreshBankBalance();

function refreshBankBalance() {
    let tokenData = loadToken();
    let token = tokenData["token"];

    const options = {
        method: "get",
        url: `http://localhost:8000/bank-balance/`,
        headers: {
            Authorization: `Token ${token}`,
        },
    };

    axios(options)
        .then((res) => {
            console.log("BALACE");
            const totalAmount = res.data.total_amount;
            console.log(totalAmount);
            const balanceElement = document.getElementById("bank-balance");
            balanceElement.innerHTML = "Balance: " + totalAmount;
        })
        .catch((e) => {
            console.log(e)
            console.log("bank balance Error!");
        });
}
function loadPendingRequests(path) {
    const token = loadToken()["token"];

    const pendingRequest = {
        method: "get",
        url: `http://localhost:8000/${path}s-pending/`,
        headers: {
            Authorization: `Token ${token}`,
        },
    };

    axios(pendingRequest)
        .then((res) => {
            console.log(res);
            let pending = res.data;
            console.log(path);
            console.log(pending);
            let data = [];

            for (let i = 0; i < pending.length; i++) {
                pending[i]["option"] = getPlanWithID(pending[i]["option"], path);
            }

            if (path == "loan") {
                pendingLoans = pending;
            } else if (path == "fund") {
                pendingFunds = pending;
            }

            listLoansOrFunds(pending, path);
        })
        .catch((e) => {
            console.log(e);
            console.log("Error loading loans pending!");
        });
}

function getPlanWithID(id, path) {
    let data = [];
    if (path == "loan") {
        data = availableLoanOptions;
    } else if (path == "fund") {
        data = availableLoanOptions;
    }
    for (let i = 0; i < data.length; i++) {
        let option = data[i];
        if (option["id"] == id) {
            return option;
        }
    }
}

function loadOptions(path) {
    let tokenData = loadToken();
    let token = tokenData["token"];

    const options = {
        method: "get",
        url: `http://localhost:8000/${path}-options/`,
        headers: {
            Authorization: `Token ${token}`,
        },
    };

    axios(options)
        .then((res) => {
            console.log(res);

            // Grab the data.
            let options = res.data;

            // Sort the list descending.
            options = options.sort(function (a, b) {
                return b["duration"] - a["duration"];
            });

            // Keep the loan options to use when changing plans.
            if (path === "loan") {
                availableLoanOptions = options;
            } else {
                availableFundOptions = options;
            }
            loadPendingRequests(path);
        })
        .catch((e) => {
            console.log(e);
            console.log("Options Error!");
        });
}

function changePendingStatus(id, path, decisionCode) {
    const token = loadToken()["token"];

    const applyDecisionRequest = {
        method: "patch",
        url: `http://localhost:8000/${path}s/${id}/`,
        headers: {
            Authorization: `Token ${token}`,
        },
        data: {
            status: decisionCode,
        },
    };

    axios(applyDecisionRequest)
        .then((res) => {
            console.log(res);
            if (res.data.message) {
                alert(res.data.message);
            }
            refreshBankBalance()
            loadPendingRequests(path);
        })
        .catch((e) => {
            console.log(e);
            console.log("Error making decision!");
        });
}

function createOption(path) {
    const token = loadToken()["token"];
    const body = collectOptionData();

    const createLoanOptionRequest = {
        method: "post",
        url: `http://localhost:8000/${path}-options/`,
        headers: {
            Authorization: `Token ${token}`,
        },
        data: body,
    };

    axios(createLoanOptionRequest)
        .then((res) => {
            console.log(res);
            if (res.statusText) {
                alert(res.statusText);
            }
        })
        .catch((e) => {
            console.log(e);
            console.log("Error creating loan option!");
        });
}

function collectOptionData() {
    let minAmountElement = document.getElementById("minAmount");
    let maxAmountElement = document.getElementById("maxAmount");
    let interestElement = document.getElementById("interest");
    let durationElement = document.getElementById("months");

    return {
        minimum_amount: Number(minAmountElement.value),
        maximum_amount: Number(maxAmountElement.value),
        duration: Number(durationElement.value),
        interest_rate: Number(interestElement.value),
    };
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

function listLoansOrFunds(data, path) {
    let table = document.getElementById(`${path}sTable`);
    let tbody = table.createTBody();

    table.innerHTML = "";
    let th = tbody.insertRow();
    th.insertCell().innerHTML = "Amount";
    th.insertCell().innerHTML = "Duration";
    th.insertCell().innerHTML = "Started";
    th.insertCell().innerHTML = "Decision";

    for (let i = 0; i < data.length; i++) {
        const loan = data[i];
        let row = tbody.insertRow();

        row.insertCell().innerHTML = loan["amount"];
        row.insertCell().innerHTML = loan["option"]["duration"] + " Months";
        row.insertCell().innerHTML = loan["started"].split("T")[0];

        let decisionCell = row.insertCell(3);
        let approveButton = document.createElement("button");
        approveButton.className = "button";
        approveButton.innerText = "Approve";
        approveButton.setAttribute("onclick", `applyDecision(${i}, ${path == "loan" ? 1 : 2}, "Approved");`);

        let denyButton = document.createElement("button");
        denyButton.className = "button-reject";
        denyButton.innerText = "Deny";
        denyButton.setAttribute("onclick", `applyDecision(${i}, ${path == "loan" ? 1 : 2}, "Denied");`);

        decisionCell.appendChild(approveButton);
        decisionCell.appendChild(denyButton);
    }

    table.appendChild(tbody);
}

function applyDecision(rowIndex, numericPath, decision) {
    const DECISION_CODE = {
        Approved: 2,
        Denied: 3,
    };
    let path = numericPath == 1 ? "loan" : "fund";
    let data = path == "loan" ? pendingLoans[rowIndex] : pendingFunds[rowIndex];

    changePendingStatus(data["id"], path, DECISION_CODE[decision]);
}

let minSlider = document.getElementById("minRangeSlider");
let minAmount = document.getElementById("minAmount");

minSlider.oninput = function () {
    minAmount.value = minSlider.value;
};

let maxSlider = document.getElementById("maxRangeSlider");
let maxAmount = document.getElementById("maxAmount");

maxSlider.oninput = function () {
    maxAmount.value = maxSlider.value;
};

document.getElementById("createLoanOptionRequestButton").setAttribute("onclick", `createOption("loan")`);
document.getElementById("createFundOptionRequestButton").setAttribute("onclick", `createOption("fund")`);

let modal = document.getElementById("createOptionForm");
let btn = document.getElementById("createOptionBtn");
let span = document.getElementsByClassName("close")[0];
btn.onclick = function () {
    modal.style.display = "block";
};
span.onclick = function () {
    modal.style.display = "none";
};
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

function logout() {
    localStorage.clear();
    console.log(localStorage.getItem("user"));
    window.location.href = "../Login.html";
}
