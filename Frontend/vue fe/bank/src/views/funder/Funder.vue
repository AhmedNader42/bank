<template>
    <v-app>
        <FunderNav />
        <div class="container-fluid">
            <div class="row">
                <FunderMenu />

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
import FunderNav from "@/components/funder/FunderNav.vue";
import FunderMenu from "@/components/funder/FunderMenu.vue";

export default {
    name: "Funder",
    components: { FunderNav, FunderMenu },

    data() {
        return {
            username: localStorage.username,
            token: localStorage.token,
        };
    },
};
</script>
