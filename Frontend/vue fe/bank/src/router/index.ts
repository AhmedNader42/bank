import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import NProgress from "nprogress";

import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import Customer from "@/views/customer/Customer.vue";
import Loans from "@/views/customer/Loans.vue";
import CreateLoan from "@/views/customer/CreateLoan.vue";

import Funder from "@/views/funder/Funder.vue";
import Funds from "@/views/funder/Funds.vue";
import CreateFund from "@/views/funder/CreateFund.vue";

import Banker from "@/views/banker/Banker.vue";
import PendingLoans from "@/views/banker/PendingLoans.vue";
import PendingFunds from "@/views/banker/PendingFunds.vue";
import CreateLoanOption from "@/views/banker/CreateLoanOption.vue";
import CreateFundOption from "@/views/banker/CreateFundOption.vue";
import SystemReport from "@/views/banker/SystemReport.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
    {
        path: "",
        redirect: "/login",
    },
    {
        path: "/customer",
        component: Customer,
        children: [
            {
                path: "",
                redirect: "/myloans",
            },
            {
                path: "/myloans",
                component: Loans,
            },
            {
                path: "/createloan",
                component: CreateLoan,
            },
        ],
    },
    {
        path: "/funder",
        component: Funder,
        children: [
            {
                path: "",
                redirect: "/myfunds",
            },
            {
                path: "/myfunds",
                component: Funds,
            },
            {
                path: "/createfund",
                component: CreateFund,
            },
        ],
    },
    {
        path: "/banker",
        component: Banker,
        children: [
            {
                path: "",
                redirect: "/pending-loans",
            },
            {
                path: "/pending-loans",
                component: PendingLoans,
            },
            {
                path: "/pending-funds",
                component: PendingFunds,
            },
            {
                path: "/create-loan-option",
                component: CreateLoanOption,
            },
            {
                path: "/create-fund-option",
                component: CreateFundOption,
            },
            {
                path: "/system-report",
                component: SystemReport,
            },
        ],
    },
    {
        path: "/login",
        component: Login,
    },
    {
        path: "/register",
        component: Register,
    },
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});
export default router;
