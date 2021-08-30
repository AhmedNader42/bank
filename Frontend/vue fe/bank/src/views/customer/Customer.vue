<template>
    <v-app>
        <CustomerNav />
        <div class="container-fluid">
            <div class="row">
                <CustomerMenu />

                <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                    <div class="table-responsive">
                        <router-view />
                    </div>
                </main>
            </div>
        </div>
    </v-app>
</template>

<script>
import CustomerNav from "@/components/customer/CustomerNav.vue";
import CustomerMenu from "@/components/customer/CustomerMenu.vue";

export default {
    name: "Customer",
    components: { CustomerNav, CustomerMenu },

    data() {
        return {
            username: localStorage.username,
            token: localStorage.token,
        };
    },
};
</script>
