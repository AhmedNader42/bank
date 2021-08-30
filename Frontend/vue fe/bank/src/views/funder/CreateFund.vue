<template>
    <v-expansion-panels popout focusable>
        <v-expansion-panel v-for="fundOption in fundOptions" :key="fundOption.id">
            <v-expansion-panel-header>
                {{ fundOption.duration }} Months Plan - {{ fundOption.interest_rate }}% interest
                rate</v-expansion-panel-header
            >
            <v-expansion-panel-content>
                <v-text-field
                    label="Minimum Amount"
                    type="number"
                    disabled
                    v-bind:value="fundOption.minimum_amount"
                    prefix="$"
                ></v-text-field>
                <v-text-field
                    label="Maximum Amount"
                    type="number"
                    disabled
                    v-bind:value="fundOption.maximum_amount"
                    prefix="$"
                ></v-text-field>
                <v-text-field
                    label="Amount Needed"
                    type="number"
                    v-model="requested_amount"
                    v-bind:value="fundOption.minimum_amount"
                    prefix="$"
                ></v-text-field>
                <v-btn
                    class="ma-2"
                    :loading="loading"
                    :disabled="loading"
                    color="secondary"
                    @click="createFund(fundOption)"
                >
                    Request Fund
                </v-btn>
            </v-expansion-panel-content>
        </v-expansion-panel>
    </v-expansion-panels>
</template>

<script>
import axios from 'axios';

export default {
    name: 'CreateFund',
    data() {
        return {
            fundOptions: [],
            loading: false,
            requested_amount: 0.0,
        };
    },
    async mounted() {
        this.loadFundOptions();
    },
    methods: {
        async loadFundOptions() {
            const token = localStorage.getItem('token');

            const fundOptions = {
                method: 'get',
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
                    return b['duration'] - a['duration'];
                });

                // Keep the fund options to use when changing plans.
                this.fundOptions = options;
            } catch (error) {
                console.log(error);
                this.$toast.error('Error getting fund options ' + error);
            }
        },
        async createFund(fundOption) {
            if (
                Number(this.requested_amount) < Number(fundOption.minimum_amount - 1) ||
                Number(this.requested_amount) > Number(fundOption.maximum_amount)
            ) {
                this.$toast.error("Fund option selected doesn't support amount requested.");
                return;
            }

            const token = localStorage.getItem('token');
            const user = JSON.parse(localStorage.getItem('user'));

            this.loading = true;
            const createFund = {
                method: 'post',
                url: `funds/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
                data: {
                    funder: user.id,
                    amount: Number(this.requested_amount),
                    option: fundOption.id,
                },
            };

            try {
                const response = await axios(createFund);
                this.$toast.success('Successfully Requested Fund.');
            } catch (error) {
                this.$toast.error('Creating fund Error.');
            }
            this.loading = false;
        },
    },
};
</script>
