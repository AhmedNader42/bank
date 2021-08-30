<template>
    <v-app>
        <div class="iCountUp"><ICountUp :delay="delay" :endVal="numberOfUsers" /> Users</div>
        <v-toolbar class="h1">
            <v-spacer></v-spacer>
            <div><ICountUp :delay="delay" :endVal="numberOfBankers" /> Bankers</div>
            <v-spacer></v-spacer>
            <div>
                <ICountUp :delay="delay" :endVal="numberOfCustomers" />
                Customers
            </div>
            <v-spacer></v-spacer>
            <div><ICountUp :delay="delay" :endVal="numberOfFunders" /> Funders</div>
            <v-spacer></v-spacer>
        </v-toolbar>
        <div class="iCountUp"><ICountUp :delay="delay" :endVal="numberOfLoans" /> Loans</div>
        <v-toolbar class="h1">
            <v-spacer></v-spacer>
            <div class="text-success"><ICountUp :delay="delay" :endVal="approvedLoans" /> Approved</div>
            <v-spacer></v-spacer>
            <div class="text-warning">
                <ICountUp :delay="delay" :endVal="pendingLoans" />
                Pending
            </div>
            <v-spacer></v-spacer>
            <div class="text-danger"><ICountUp :delay="delay" :endVal="deniedLoans" /> Denied</div>
            <v-spacer></v-spacer>
        </v-toolbar>
        <div class="iCountUp"><ICountUp :delay="delay" :endVal="numberOfFunds" /> Funds</div>
        <v-toolbar class="h1">
            <v-spacer></v-spacer>
            <div class="text-success"><ICountUp :delay="delay" :endVal="approvedFunds" /> Approved</div>
            <v-spacer></v-spacer>
            <div class="text-warning">
                <ICountUp :delay="delay" :endVal="pendingFunds" />
                Pending
            </div>
            <v-spacer></v-spacer>
            <div class="text-danger"><ICountUp :delay="delay" :endVal="deniedFunds" /> Denied</div>
            <v-spacer></v-spacer>
        </v-toolbar>
    </v-app>
</template>

<script>
import axios from "axios";
import ICountUp from "vue-countup-v2";

export default {
    name: "CreateFund",
    components: {
        ICountUp,
    },
    data() {
        return {
            numberOfUsers: 0,
            numberOfBankers: 0,
            numberOfCustomers: 0,
            numberOfFunders: 0,
            numberOfLoans: 0,
            approvedLoans: 0,
            deniedLoans: 0,
            pendingLoans: 0,
            numberOfFunds: 0,
            approvedFunds: 0,
            deniedFunds: 0,
            pendingFunds: 0,

            delay: 500,
            endVal: 100,
        };
    },
    async mounted() {
        this.loadSystemReport();
    },
    methods: {
        async loadSystemReport() {
            const token = localStorage.getItem("token");

            const fundOptions = {
                method: "get",
                url: `system-report/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
            };
            try {
                const response = await axios(fundOptions);
                const data = response.data;
                console.log(data);
                this.numberOfUsers = data.total_number_of_users;
                this.numberOfBankers = data.bankers;
                this.numberOfCustomers = data.customer;
                this.numberOfFunders = data.funders;

                this.numberOfLoans = data.total_number_of_loans;
                this.pendingLoans = data.pending_loans;
                this.approvedLoans = data.approved_loans;
                this.deniedLoans = data.denied_loans;

                this.numberOfFunds = data.total_number_of_funds;
                this.pendingFunds = data.pending_funds;
                this.approvedFunds = data.approved_funds;
                this.deniedFunds = data.denied_funds;
            } catch (error) {
                console.log("Error getting system report " + error);
                this.$toast.error("Error getting system report!");
            }
        },
    },
};
</script>

<style scoped>
.iCountUp {
    font-size: 6em;
    margin: 0;
    color: #4d63bc;
}
</style>
