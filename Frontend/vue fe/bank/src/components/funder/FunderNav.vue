<template>
    <header class="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow">
        <a class="navbar-brand col-md-3 col-lg-2 me-0 px-3" href="#">Bank</a>
        <nav class="my-2 my-md-0 mr-md-3">
            <a href="#" class="p-2 text-white text-decoration-none"> {{ user.email }}</a>
            <a href="#" @click="logout" class="p-2 text-white text-decoration-none">Sign out</a>
        </nav>
    </header>
</template>

<script>
import { User } from "../../models/User";
export default {
    name: "FunderNav",
    data() {
        const user = JSON.parse(localStorage.getItem("user")) ?? new User();
        return {
            user: user,
        };
    },
    methods: {
        logout() {
            console.log("Logout");
            localStorage.clear();
            this.$router.push("/login");
        },
    },
};
</script>
