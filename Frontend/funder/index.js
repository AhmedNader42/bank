"use strict";
loadToken();
loadFundOptions();

let availableFundOptions = [];
let availableUserFunds = [];

function loadUserFunds() {
    const user = JSON.parse(localStorage.getItem("user"));
    const token = loadToken()["token"];

    console.log(user["pk"])
    const funderFunds = {
        method: "get",
        url: `http://localhost:8000/funder/${user["pk"]}/`,
        headers: {
            Authorization: `Token ${token}`,
        },
    };

    axios(funderFunds)
        .then((res) => {
            console.log(res);
            availableUserFunds = res.data;
            for (let i = 0; i < availableUserFunds.length; i++) {
                availableUserFunds[i]["option"] = getPlanWithID(availableUserFunds[i]["option"]);
            }
            listFunds(res.data);
        })
        .catch((e) => {
            alert("Error loading funds!");
        });
}

function loadFundOptions() {
    let tokenData = loadToken();
    let token = tokenData["token"];

    const fundOptions = {
        method: "get",
        url: `http://localhost:8000/fund-options/`,
        headers: {
            Authorization: `Token ${token}`,
        },
    };

    axios(fundOptions)
        .then((res) => {
            console.log(res);

            // Grab the data.
            let fundOptions = res.data;

            // Sort the list descending.
            fundOptions = fundOptions.sort(function (a, b) {
                return b["duration"] - a["duration"];
            });

            // Keep the fund options to use when changing plans.
            availableFundOptions = fundOptions;

            // Grab the select element.
            var select = document.getElementById("fundOptions");

            // Empty any previous data.
            select.innerHTML = "";

            // Add fund options as select options.
            fundOptions.forEach((element) => {
                var option = document.createElement("option");
                let duration = element["duration"];
                option.value = element["id"];
                option.innerHTML = duration;
                select.appendChild(option);
            });

            // Update the rest of the elements to show the selected default
            selectedFundOption();

            // Load the user funds
            loadUserFunds();
        })
        .catch((e) => {
            alert("FundOptions Error!");
        });
}

function createFundRequest() {
    let select = document.getElementById("fundOptions");
    let selectedPlan = getPlanWithID(select.value);
    let amount = document.getElementById("amount");
    const user = JSON.parse(localStorage.getItem("user"));
    let token = loadToken()["token"];
    
    console.log(user)
    const createFund = {
        method: "post",
        url: `http://localhost:8000/funds/`,
        headers: {
            Authorization: `Token ${token}`,
        },
        data: {
            funder: user.pk,
            amount: Number(amount.value),
            option: selectedPlan["id"],
        },
    };

    axios(createFund)
        .then((res) => {
            console.log(res);
            if (res.data.message) {
                alert(res.data.message);
            }
            loadUserFunds();
        })
        .catch((e) => {
            console.log(e);
            alert("Creating fund Error!");
        });
}

function listFunds() {
    let table = document.getElementById("fundsTable");
    let thead = table.createTHead();
    let tbody = table.createTBody();
    const FUND_STATUS = {
        1: {
            state: "PENDING",
            color: "gray",
        },
        2: {
            state: "APPROVED",
            color: "green",
        },
        3: {
            state: "DENIED",
            color: "red",
        },
    };

    table.innerHTML = "";
    let th = tbody.insertRow();
    th.insertCell().innerHTML = "Amount";
    th.insertCell().innerHTML = "Duration";
    th.insertCell().innerHTML = "Started";
    th.insertCell().innerHTML = "Status";

    for (let i = 0; i < availableUserFunds.length; i++) {
        const fund = availableUserFunds[i];
        let row = tbody.insertRow();

        row.setAttribute("onclick", "showAmortizationTableForCell(" + i + ");");

        row.insertCell().innerHTML = fund["amount"];
        row.insertCell().innerHTML = fund["option"]["duration"] + " Months";
        row.insertCell().innerHTML = fund["started"].split("T")[0];

        let statusCell = row.insertCell();
        let fundStatus = FUND_STATUS[fund["status"]];
        statusCell.innerHTML = fundStatus["state"];
        statusCell.style.backgroundColor = fundStatus["color"];
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

function selectedFundOption() {
    let select = document.getElementById("fundOptions");
    let interest = document.getElementById("interest");
    let minAmount = document.getElementById("minAmount");
    let maxAmount = document.getElementById("maxAmount");
    let rangeSlider = document.getElementById("rangeSlider");
    let amount = document.getElementById("amount");

    let selectedPlan = getPlanWithID(select.value);
    console.log(selectedPlan);
    let minAmountOfMoney = selectedPlan["minimum_amount"].split(".")[0];
    let maxAmountOfMoney = selectedPlan["maximum_amount"].split(".")[0];

    interest.innerText = "Interest : " + selectedPlan["interest_rate"] + "%";
    minAmount.innerText = "Minimum Amount : " + minAmountOfMoney + "$";
    maxAmount.innerText = "Maximum Amount : " + maxAmountOfMoney + "$";

    amount.min = minAmountOfMoney;
    amount.max = maxAmountOfMoney;
    amount.value = minAmountOfMoney;

    rangeSlider.min = minAmountOfMoney;
    rangeSlider.max = maxAmountOfMoney;
    rangeSlider.value = minAmountOfMoney;
}

function getPlanWithID(id) {
    for (let i = 0; i < availableFundOptions.length; i++) {
        let fundOption = availableFundOptions[i];
        if (fundOption["id"] == id) {
            return fundOption;
        }
    }
}
var btn = document.getElementById("createFundRequestBtn");
createFundRequestButton.onclick = function () {
    createFundRequest();
};

var modal = document.getElementById("createFundForm");
var btn = document.getElementById("createFundBtn");
var span = document.getElementsByClassName("close")[0];
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

var slider = document.getElementById("rangeSlider");
var output = document.getElementById("amount");

slider.oninput = function () {
    output.value = this.value;
};

function showAmortizationTableForCell(rowIndex) {
    let fund = availableUserFunds[rowIndex];
    let fundOptions = fund["option"];
    let amortizationTable = document.getElementById("amortizationTable");
    console.log(fund);
    amortizationTable.innerHTML = "";
    amortizationTable.innerHTML = amort(
        Number(fund["amount"]),
        fundOptions["interest_rate"] / 100,
        fundOptions["duration"]
    );
}
function amort(balance, interestRate, terms) {
    //Calculate the per month interest rate
    var monthlyRate = interestRate / 12;

    //Calculate the payment
    var payment = balance * (monthlyRate / (1 - Math.pow(1 + monthlyRate, -terms)));

    //begin building the return string for the display of the amort table
    var result =
        "Fund amount: $" +
        balance.toFixed(2) +
        "<br />" +
        "Interest rate: " +
        (interestRate * 100).toFixed(2) +
        "%<br />" +
        "Number of months: " +
        terms +
        "<br />" +
        "Monthly payment: $" +
        payment.toFixed(2) +
        "<br />" +
        "Total paid: $" +
        (payment * terms).toFixed(2) +
        "<br /><br />";

    //add header row for table to return string
    result +=
        "<table border='1' width='100%'><tr><th>Month #</th><th>Balance</th>" + "<th>Interest</th><th>Principal</th>";

    /**
     * Loop that calculates the monthly Fund amortization amounts then adds
     * them to the return string
     */
    for (var count = 0; count < terms; ++count) {
        //in-loop interest amount holder
        var interest = 0;

        //in-loop monthly principal amount holder
        var monthlyPrincipal = 0;

        //start a new table row on each loop iteration
        result += "<tr align=center>";

        //display the month number in col 1 using the loop count variable
        result += "<td>" + (count + 1) + "</td>";

        //code for displaying in loop balance
        result += "<td> $" + balance.toFixed(2) + "</td>";

        //calc the in-loop interest amount and display
        interest = balance * monthlyRate;
        result += "<td> $" + interest.toFixed(2) + "</td>";

        //calc the in-loop monthly principal and display
        monthlyPrincipal = payment - interest;
        result += "<td> $" + monthlyPrincipal.toFixed(2) + "</td>";

        //end the table row on each iteration of the loop
        result += "</tr>";

        //update the balance for each loop iteration
        balance = balance - monthlyPrincipal;
    }

    //Final piece added to return string before returning it - closes the table
    result += "</table>";

    //returns the concatenated string to the page
    return result;
}

let amortTable = document.getElementById("amortizationTable");
let amortHTML = amort(10000, 10, 12);
amortTable.innerHTML += amortHTML;
