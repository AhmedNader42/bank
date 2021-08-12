"use strict";
loadLoanOptions();

let availableLoanOptions = [];
let availableUserLoans = [];

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
            availableUserLoans = res.data;
            for (let i = 0; i < availableUserLoans.length; i++) {
                availableUserLoans[i]["loan_type"] = getPlanWithID(availableUserLoans[i]["loan_type"]);
            }
            listLoans(res.data);
        })
        .catch((e) => {
            alert("Error loading loans!");
        });
}

function loadLoanOptions() {
    let tokenData = loadToken();
    let token = tokenData["token"];

    const loanOptions = {
        method: "get",
        url: `http://localhost:8000/loan-options/`,
        headers: {
            Authorization: `Token ${token}`,
        },
    };

    axios(loanOptions)
        .then((res) => {
            console.log(res);

            // Grab the data.
            let loanOptions = res.data;

            // Sort the list descending.
            loanOptions = loanOptions.sort(function (a, b) {
                return b["duration"] - a["duration"];
            });

            // Keep the loan options to use when changing plans.
            availableLoanOptions = loanOptions;

            // Grab the select element.
            var select = document.getElementById("loanOptions");

            // Empty any previous data.
            select.innerHTML = "";

            // Add loan options as select options.
            loanOptions.forEach((element) => {
                var option = document.createElement("option");
                let duration = element["duration"];
                option.value = element["id"];
                option.innerHTML = duration;
                select.appendChild(option);
            });

            // Update the rest of the elements to show the selected default
            selectedLoanOption();

            // Load the user loans
            loadUserLoans();
        })
        .catch((e) => {
            alert("LoanOptions Error!");
        });
}

function createLoanRequest() {
    let selectedPlan = getPlanWithID();
    let amount = document.getElementById("amount");
    const user = JSON.parse(localStorage.getItem("user"));
    let token = loadToken()["token"];

    const createLoan = {
        method: "post",
        url: `http://localhost:8000/loans/`,
        headers: {
            Authorization: `Token ${token}`,
        },
        data: {
            customer: user.id,
            amount: Number(amount.value),
            loan_type: selectedPlan["id"],
        },
    };

    axios(createLoan)
        .then((res) => {
            console.log(res);
            if (res.data.message) {
                alert(res.data.message);
            }
        })
        .catch((e) => {
            console.log(e);
            alert("Creating loan Error!");
        });
}

function listLoans() {
    let table = document.getElementById("loansTable");
    let thead = table.createTHead();
    let tbody = table.createTBody();
    const LOAN_STATUS = {
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
    let th = thead.insertRow(0);
    th.insertCell(0).innerHTML = "Amount";
    th.insertCell(1).innerHTML = "Duration";
    th.insertCell(2).innerHTML = "Started";
    th.insertCell(3).innerHTML = "Status";

    for (let i = 0; i < availableUserLoans.length; i++) {
        const loan = availableUserLoans[i];
        let row = tbody.insertRow(i);

        row.setAttribute("onclick", "showAmortizationTableForCell(" + i + ");");

        row.insertCell(0).innerHTML = loan["amount"];
        row.insertCell(1).innerHTML = loan["loan_type"]["duration"] + " Months";
        row.insertCell(2).innerHTML = loan["started"].split("T")[0];

        let statusCell = row.insertCell(3);
        let loanStatus = LOAN_STATUS[loan["status"]];
        statusCell.innerHTML = loanStatus["state"];
        statusCell.style.backgroundColor = loanStatus["color"];
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

function selectedLoanOption() {
    let select = document.getElementById("loanOptions");
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
    for (let i = 0; i < availableLoanOptions.length; i++) {
        let loanOption = availableLoanOptions[i];
        if (loanOption["id"] == id) {
            return loanOption;
        }
    }
}
var btn = document.getElementById("createLoanRequestBtn");
createLoanRequestButton.onclick = function () {
    createLoanRequest();
};

var modal = document.getElementById("createLoanForm");
var btn = document.getElementById("createLoanBtn");
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
    let loan = availableUserLoans[rowIndex];
    let loanOptions = loan["loan_type"];
    let amortizationTable = document.getElementById("amortizationTable");
    console.log(loan);
    amortizationTable.innerHTML = "";
    amortizationTable.innerHTML = amort(Number(loan["amount"]), loanOptions["interest_rate"]/100, loanOptions["duration"]);
}
function amort(balance, interestRate, terms) {
    //Calculate the per month interest rate
    var monthlyRate = interestRate / 12;

    //Calculate the payment
    var payment = balance * (monthlyRate / (1 - Math.pow(1 + monthlyRate, -terms)));

    //begin building the return string for the display of the amort table
    var result =
        "Loan amount: $" +
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
    result += "<table border='1' width='100%'><tr><th>Month #</th><th>Balance</th>" + "<th>Interest</th><th>Principal</th>";

    /**
     * Loop that calculates the monthly Loan amortization amounts then adds
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
