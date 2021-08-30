<template>
    <div>
        <v-data-table
            :headers="loanHeaders"
            :items="loans"
            :single-expand="singleExpand"
            :expanded.sync="expanded"
            item-key="id"
            @click:row="rowClick"
            class="elevation-1"
        >
            <template v-slot:top>
                <v-toolbar prominent dark>
                    <v-toolbar-title>Pending Loans</v-toolbar-title>
                    <v-spacer></v-spacer>

                    <v-toolbar-title class="text-info">Bank Balance : {{ balance }}$</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-toolbar-title class="text-success">In : +{{ in_flow }}$</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-toolbar-title class="text-danger">Out : -{{ out_flow }}$</v-toolbar-title>
                </v-toolbar>
            </template>
            <template v-slot:expanded-item="{ headers, item }" class="text-center">
                <v-card :colspan="headers.length" style="margin:20px; padding: 20px; ">
                    <v-card-text>
                        <p>Amount Requested => {{ item.amount }}</p>
                        <p>Interest Rate => {{ item.option.interest_rate }}%</p>
                        <p>Duration => {{ item.option.duration }} Months</p>
                        <p>started => {{ item.started }}</p>
                        <p>Generated inflow => {{ item.inflow_increase }}</p>
                    </v-card-text>
                    <semipolar-spinner v-if="loading" :animation-duration="2000" :size="65" color="#ff1d5e" />
                    <v-card-actions v-if="!loading">
                        <v-btn text color="blue accent-4" @click="makeDecision(item, 2)">
                            Approve
                        </v-btn>
                        <v-btn text color="red accent-4" @click="makeDecision(item, 3)">
                            Deny
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </template>
        </v-data-table>
    </div>
</template>

<script>
import axios from "axios";
import { SemipolarSpinner } from "epic-spinners";

export default {
    name: "Loans",
    components: {
        SemipolarSpinner,
    },
    data() {
        return {
            loans: [],
            loanOptions: [],
            balance: 0.0,
            in_flow: 0.0,
            out_flow: 0.0,
            loading: false,
            loanHeaders: [
                {
                    text: "Amount",
                    align: "start",
                    sortable: true,
                    value: "amount",
                },
                { text: "Started", value: "started" },
                { text: "Generated inflow", value: "inflow_increase" },
                { text: "Status", value: "status" },
                { text: "", value: "data-table-expand" },
            ],
            loanStatus: {
                1: "PENDING",
                2: "APPROVED",
                3: "DENIED",
            },
            expanded: [],
            singleExpand: true,
        };
    },
    async mounted() {
        this.refreshBankBalance();
        await this.loadLoanOptions();
    },
    methods: {
        async loadLoanOptions() {
            const token = localStorage.getItem("token");

            const loanOptions = {
                method: "get",
                url: `loan-options/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
            };
            try {
                const response = await axios(loanOptions);

                // Grab the data.
                let options = response.data;

                // Sort the list descending.
                options = options.sort(function(a, b) {
                    return b["duration"] - a["duration"];
                });

                // Keep the loan options to use when changing plans.
                this.loanOptions = options;

                // Start loading the user loans
                this.loadPendingLoans();
            } catch (error) {
                console.log("Error getting loan options " + error);
                this.$toast.error("Error getting loan options!");
            }
        },
        async loadPendingLoans() {
            const token = localStorage.getItem("token");

            const loadUserLoans = {
                method: "get",
                url: `loans-pending/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
            };
            try {
                let { data } = await axios(loadUserLoans);
                let formattedLoans = [];
                data.forEach((loan) => {
                    let loanFormatted = {
                        id: loan.id,
                        amount: loan.amount,
                        started: loan.started.split("T")[0],
                        status: this.loanStatus[loan.status],
                        payment_url: loan.payment_url,
                        option: this.getPlanWithID(loan.option),
                        inlow_increase: 0,
                    };

                    const interestRate = loanFormatted.option.interest_rate / 100;
                    const amount = loanFormatted.amount;
                    const terms = loanFormatted.option.duration;

                    let monthlyRate = interestRate / 12;
                    console.log(monthlyRate);

                    //Calculate the payment
                    let payment = amount * (monthlyRate / (1 - Math.pow(1 + monthlyRate, -terms)));

                    loanFormatted.inflow_increase = payment * terms - amount;
                    console.log(loanFormatted);
                    formattedLoans.push(loanFormatted);
                });
                this.loans = formattedLoans;
            } catch (error) {
                this.$toast.error("Error loading loans!");
                console.log(error);
            }
        },
        rowClick(_, slot) {
            if (slot.isExpanded) {
                slot.expand(!slot.isExpanded);
                return;
            } else {
                slot.expand(!slot.isExpanded);
            }
        },
        getPlanWithID(id) {
            for (let i = 0; i < this.loanOptions.length; i++) {
                let loanOption = this.loanOptions[i];
                if (loanOption["id"] == id) {
                    return loanOption;
                }
            }
        },
        async makeDecision(loan, decision) {
            this.loading = true;
            const token = localStorage.getItem("token");

            const applyDecisionRequest = {
                method: "patch",
                url: `loans/${loan.id}/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
                data: {
                    status: decision,
                },
            };

            try {
                const response = await axios(applyDecisionRequest);
                console.log(response);
                this.refreshBankBalance();
                this.loadPendingLoans();
            } catch (e) {
                console.log(e);
                this.$toast.error("Can't apply decision! Check the balance.");
            }
            this.loading = false;
        },

        refreshBankBalance() {
            let token = localStorage.getItem("token");

            const options = {
                method: "get",
                url: `bank-balance/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
            };

            axios(options)
                .then((res) => {
                    console.log("BALANCE");
                    const bank = res.data;
                    console.log(bank);
                    this.balance = bank.total_amount;
                    this.in_flow = bank.in_flow;
                    this.out_flow = bank.out_flow;
                })
                .catch((e) => {
                    console.log(e);
                    this.$toast.error("Error getting bank balance!");
                });
        },
    },
};
</script>
