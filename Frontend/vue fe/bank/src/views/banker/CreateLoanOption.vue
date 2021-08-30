<template>
    <v-app>
        <p>Available Loan Options</p>
        <v-expansion-panels popout focusable>
            <v-expansion-panel v-for="loanOption in loanOptions" :key="loanOption.id">
                <v-expansion-panel-header>
                    {{ loanOption.duration }} Months Plan - {{ loanOption.interest_rate }}% interest
                    rate</v-expansion-panel-header
                >
                <v-expansion-panel-content>
                    <v-text-field
                        label="Minimum Amount"
                        disabled
                        v-bind:value="loanOption.minimum_amount"
                        prefix="$"
                    ></v-text-field>
                    <v-text-field
                        label="Maximum Amount"
                        disabled
                        v-bind:value="loanOption.maximum_amount"
                        prefix="$"
                    ></v-text-field>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
        <v-form ref="form" lazy-validation>
            <v-text-field
                v-model="minimumAmount"
                type="number"
                :counter="2"
                label="Minimun Amount"
                required
            ></v-text-field>

            <v-text-field
                v-model="maximumAmount"
                type="number"
                :counter="15"
                label="Maximum Amount"
                required
            ></v-text-field>
            <v-text-field v-model="interestRate" type="number" label="Interest Rate" required></v-text-field>
            <v-text-field v-model="months" type="number" label="Months" required></v-text-field>

            <v-btn color="primary" class="mr-4" @click="createLoanOption">
                Create Loan Option
            </v-btn>
        </v-form>
    </v-app>
</template>

<script>
import axios from "axios";

export default {
    name: "CreateLoan",
    data() {
        return {
            loanOptions: [],
            loading: false,
            requested_amount: 0.0,
            minimumAmount: 0,
            maximumAmount: 0,
            interestRate: 0,
            months: 0,
        };
    },
    async mounted() {
        this.loadLoanOptions();
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
            } catch (error) {
                console.log("Error getting loan options " + error);
                this.$toast.error("Error getting loan options!");
            }
        },
        async createLoanOption() {
            const token = localStorage.getItem("token");
            let minimum_amount = Number(this.minimumAmount);
            let maximum_amount = Number(this.maximumAmount);
            let duration = Number(this.months);
            let interest_rate = Number(this.interestRate);

            if (!minimum_amount || minimum_amount < 0) {
                this.$toast.error("Enter correct minimum amount");
                return;
            }

            if (!maximum_amount || maximum_amount < 0 || maximum_amount <= minimum_amount) {
                this.$toast.error("Enter correct maxmimum amount");
                return;
            }

            if (!interest_rate || interest_rate > 100 || interest_rate < 1) {
                this.$toast.error("Enter correct interest amount within 1-100");
                return;
            }

            if (!duration || duration < 0) {
                this.$toast.error("Enter correct Months amount");
                return;
            }
            const createLoanOptionRequest = {
                method: "post",
                url: `loan-options/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
                data: {
                    minimum_amount: minimum_amount,
                    maximum_amount: maximum_amount,
                    duration: duration,
                    interest_rate: interest_rate,
                },
            };

            axios(createLoanOptionRequest)
                .then((res) => {
                    if (res.statusText) {
                        this.$toast.success(res.statusText);
                    }
                    this.loadLoanOptions();
                })
                .catch((e) => {
                    console.log(e);
                    this.$toast.error("Erorr creating loan option");
                });
        },
    },
};
</script>
