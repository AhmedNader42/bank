<template>
    <v-app>
        <BankerNav />
        <div class="container-fluid">
            <div class="row">
                <BankerMenu />

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
import BankerNav from "@/components/banker/BankerNav.vue";
import BankerMenu from "@/components/banker/BankerMenu.vue";

export default {
    name: "Banker",
    components: { BankerNav, BankerMenu },

    data() {
        return {
            username: localStorage.username,
            token: localStorage.token,
        };
    },
};
</script>
