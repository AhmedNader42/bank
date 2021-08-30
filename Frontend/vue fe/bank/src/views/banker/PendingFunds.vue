<template>
    <div>
        <v-data-table
            :headers="fundHeaders"
            :items="funds"
            :single-expand="singleExpand"
            :expanded.sync="expanded"
            @click:row="rowClick"
            item-key="id"
            class="elevation-1"
        >
            <template v-slot:top>
                <v-toolbar prominent dark>
                    <v-toolbar-title>Pending Funds</v-toolbar-title>
                    <v-spacer></v-spacer>

                    <v-toolbar-title class="text-info">Bank Balance : {{ balance }}$</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-toolbar-title class="text-success">In : +{{ in_flow }}$</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-toolbar-title class="text-danger">Out : -{{ out_flow }}$</v-toolbar-title>
                </v-toolbar>
            </template>
            <template v-slot:expanded-item="{ item }" class="text-center">
                <v-card style="margin:20px; padding: 20px; ">
                    <v-card-text>
                        <p>Amount Requested => {{ item.amount }}</p>
                        <p>Interest Rate => {{ item.option.interest_rate }}%</p>
                        <p>Duration => {{ item.option.duration }} Months</p>
                        <p>started => {{ item.started }}</p>
                        <p>Generated outflow => {{ item.outflow_increase }}</p>
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
    name: "Funds",
    components: {
        SemipolarSpinner,
    },
    data() {
        return {
            funds: [],
            fundOptions: [],
            balance: 0.0,
            in_flow: 0.0,
            out_flow: 0.0,
            loading: false,
            fundHeaders: [
                {
                    text: "Amount",
                    align: "start",
                    sortable: true,
                    value: "amount",
                },
                { text: "Started", value: "started" },
                { text: "Generated Outflow", value: "outflow_increase" },
                { text: "Status", value: "status" },
                { text: "", value: "data-table-expand" },
            ],
            fundStatus: {
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
        await this.loadFundOptions();
    },
    methods: {
        async loadFundOptions() {
            const token = localStorage.getItem("token");

            const fundOptions = {
                method: "get",
                url: `fund-options/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
            };
            try {
                const response = await axios(fundOptions);

                // Grab the data.
                let options = response.data;

                // Sort the list descending.
                options = options.sort(function(a, b) {
                    return b["duration"] - a["duration"];
                });

                // Keep the fund options to use when changing plans.
                this.fundOptions = options;

                // Start loading the user funds
                this.loadPendingFunds();
            } catch (error) {
                console.log("Error getting fund options " + error);
                this.$toast.error("Error getting fund options!");
            }
        },
        async loadPendingFunds() {
            console.log(this.funds);
            const token = localStorage.getItem("token");

            const loadUserFunds = {
                method: "get",
                url: `funds-pending/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
            };
            try {
                let { data } = await axios(loadUserFunds);
                let formattedFunds = [];
                data.forEach((fund) => {
                    let fundFormatted = {
                        id: fund.id,
                        amount: fund.amount,
                        started: fund.started.split("T")[0],
                        status: this.fundStatus[fund.status],
                        payment_url: fund.payment_url,
                        option: this.getPlanWithID(fund.option),
                        outflow_increase: 0,
                    };

                    const interestRate = fundFormatted.option.interest_rate / 100;
                    const amount = fundFormatted.amount;
                    const terms = fundFormatted.option.duration;

                    let monthlyRate = interestRate / 12;
                    console.log(monthlyRate);

                    //Calculate the payment
                    let payment = amount * (monthlyRate / (1 - Math.pow(1 + monthlyRate, -terms)));

                    fundFormatted.outflow_increase = payment * terms - amount;
                    console.log(fundFormatted);
                    formattedFunds.push(fundFormatted);
                });
                this.funds = formattedFunds;
            } catch (error) {
                console.log(error);
                this.$toast.error("Error getting funds!");
            }
        },
        getPlanWithID(id) {
            for (let i = 0; i < this.fundOptions.length; i++) {
                let fundOption = this.fundOptions[i];
                if (fundOption["id"] == id) {
                    return fundOption;
                }
            }
        },
        async makeDecision(fund, decision) {
            console.log("Deciding on fund " + decision);
            console.log(fund);
            this.loading = true;
            const token = localStorage.getItem("token");

            const applyDecisionRequest = {
                method: "patch",
                url: `funds/${fund.id}/`,
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
                this.loadPendingFunds();
            } catch (e) {
                console.log(e);
                this.$toast.error("Can't apply decision! Check the outflow generated.");
            }
            this.loading = false;
        },
        rowClick(_, slot) {
            if (slot.isExpanded) {
                slot.expand(!slot.isExpanded);
                return;
            } else {
                slot.expand(!slot.isExpanded);
            }
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
                    const bank = res.data;
                    this.balance = bank.total_amount;
                    this.in_flow = bank.in_flow;
                    this.out_flow = bank.out_flow;
                })
                .catch((e) => {
                    console.log(e);
                    this.$toast.error("bank balance Error!");
                });
        },
    },
};
</script>
