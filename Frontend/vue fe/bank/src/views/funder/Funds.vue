<template>
    <div>
        <v-data-table
            :headers="fundHeaders"
            :items="funds"
            :single-expand="singleExpand"
            :expanded.sync="expanded"
            @click:row="createAmortizationPlan"
            item-key="id"
            class="elevation-1"
        >
            <template v-slot:top>
                <v-toolbar flat>
                    <v-toolbar-title>Funds</v-toolbar-title>
                </v-toolbar>
            </template>
            <template v-slot:expanded-item="{ headers, item }">
                <!-- <td :colspan="headers.length">More info about {{ item.amount }}</td> -->
                <td :colspan="headers.length" style="margin:20px; padding: 20px;">
                    <p>Monthly : {{ currentAmortization.monthly_payment }}$</p>
                    <p>Total : {{ currentAmortization.total_payment }}$</p>
                    <v-simple-table dense style="border: solid; border-width: 1px;">
                        <template v-slot:default>
                            <thead>
                                <tr>
                                    <th class="text-left">
                                        Month
                                    </th>
                                    <th class="text-left">
                                        Balance
                                    </th>
                                    <th class="text-left">
                                        Interest
                                    </th>
                                    <th class="text-left">
                                        Principal
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="row in currentAmortization.table" :key="row.number">
                                    <td>{{ row.number }}</td>
                                    <td>{{ row.amount }} $</td>
                                    <td>{{ row.interest }} $</td>
                                    <td>{{ row.principal }} $</td>
                                </tr>
                            </tbody>
                        </template>
                    </v-simple-table>
                    <v-btn
                        v-if="item.status == `APPROVED` && item.payment_verified == false"
                        color="primary"
                        style="margin:10px; padding:10px"
                        elevation="2"
                        @click="payFundSubscription(item)"
                    >
                        Pay Now</v-btn
                    >
                    <v-btn
                        v-if="item.status == `APPROVED` && item.payment_verified == false"
                        color="primary"
                        style="margin:10px; padding:10px"
                        elevation="2"
                        @click="verifyFundPayment(item)"
                    >
                        Verify Payment</v-btn
                    >
                    <a
                        v-bind:href="item.payment_receipt_url"
                        v-if="item.status == `APPROVED` && item.payment_verified == true"
                        class="btn "
                    >
                        View Payment receipt</a
                    >
                </td>
            </template>
        </v-data-table>
    </div>
</template>

<script>
import axios from "axios";
import { loadStripe } from "@stripe/stripe-js";

export default {
    name: "Funds",
    data() {
        return {
            funds: [],
            fundOptions: [],
            currentAmortization: [],
            fundHeaders: [
                {
                    text: "Amount",
                    align: "start",
                    sortable: true,
                    value: "amount",
                },
                { text: "Started", value: "started" },
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
        if (this.$route.query.status == 0) {
            this.$toast.success("Payment successful!");
        } else if (this.$route.query.status == 1) {
            this.$toast.error("Payment Error!");
        }
        await this.loadFundOptions();
    },
    methods: {
        async payFundSubscription(fund) {
            const stripe = await loadStripe(
                "pk_test_51JQJmIDP01ev1pnVKxlhzwoTRpETICHmuMonHTEVtzUVZGCv9SzpsmaBd16GacewvzrRgpueevp27ewmKBU7cKQK007bcbJ05N"
            );
            const response = await stripe.redirectToCheckout({
                lineItems: [
                    {
                        price: fund.payment_url,
                        quantity: 1,
                    },
                ],
                mode: "payment",
                successUrl: "http://localhost:8080/myfunds?status=0",
                cancelUrl: "http://localhost:8080/myfunds?status=1",
            });
        },
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
                this.loadFunds();
            } catch (error) {
                console.log(error);
                this.$toast.error("Error getting fund options ");
            }
        },
        async verifyFundPayment(fund) {
            const token = localStorage.getItem("token");

            const verifyFund = {
                method: "post",
                url: `verify-fund/${fund.id}/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
            };
            try {
                const response = await axios(verifyFund);
                this.$toast.success("Successfully verified fund");
                this.loadFunds();
            } catch (error) {
                console.log("Error verifying fund " + error);
                this.$toast.error("Error verifying fund ");
            }
        },
        async loadFunds() {
            const user = JSON.parse(localStorage.getItem("user"));
            const token = localStorage.getItem("token");

            const loadUserFunds = {
                method: "get",
                url: `funder/${user.id}/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
            };
            try {
                let { data } = await axios(loadUserFunds);
                let formattedFunds = [];
                data.forEach((fund) => {
                    const startDate = fund.started.split("T")[0];
                    formattedFunds.push({
                        id: fund.id,
                        amount: fund.amount,
                        started: startDate,
                        status: this.fundStatus[fund.status],
                        payment_url: fund.payment_url,
                        payment_verified: fund.payment_verified,
                        payment_receipt_url: fund.payment_receipt_url,
                        option: this.getPlanWithID(fund.option),
                    });
                });
                this.funds = formattedFunds;
            } catch (error) {
                console.log(error);
                this.$toast.error("Error loading user funds ");
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
        createAmortizationPlan(fund, slot) {
            if (slot.isExpanded) {
                slot.expand(!slot.isExpanded);
                return;
            } else {
                slot.expand(!slot.isExpanded);
            }

            let amount = parseFloat(fund.amount);
            let interestRate = parseFloat(fund.option.interest_rate) / 100;
            let terms = parseInt(fund.option.duration);
            let paymentDate = new Date(fund.started);

            //Calculate the per month interest rate
            let monthlyRate = interestRate / 12;

            //Calculate the payment
            let payment = amount * (monthlyRate / (1 - Math.pow(1 + monthlyRate, -terms)));

            let amortizationData = [];
            for (var count = 0; count < terms; ++count) {
                let row = {};
                //in-loop interest amount holder
                let interest = 0;

                //in-loop monthly principal amount holder
                let monthlyPrincipal = 0;

                //display the month number in col 1 using the loop count variable
                const options = { day: "numeric", month: "long", year: "numeric" };
                row["number"] = new Intl.DateTimeFormat("en-US", options).format(paymentDate);
                paymentDate.setMonth(paymentDate.getMonth() + 1);

                //code for displaying in loop amount
                row["amount"] = amount.toFixed(2);

                //calc the in-loop interest amount and display
                interest = amount * monthlyRate;
                row["interest"] = interest.toFixed(2);

                //calc the in-loop monthly principal and display
                monthlyPrincipal = payment - interest;
                row["principal"] = monthlyPrincipal.toFixed(2);

                //update the amount for each loop iteration
                amount = amount - monthlyPrincipal;

                amortizationData.push(row);
            }

            this.currentAmortization["monthly_payment"] = payment.toFixed(2);
            this.currentAmortization["total_payment"] = (payment * terms).toFixed(2);
            this.currentAmortization["table"] = amortizationData;
        },
    },
};
</script>
