<template>
    <v-app>
        <main class="form-signin">
            <form @submit.prevent="submit">
                <h1 class="h3 mb-3 fw-normal">Register Here</h1>

                <div class="form-floating">
                    <input v-model="user_name" class="form-control" placeholder="Username" />
                    <label>Username</label>
                </div>

                <div class="form-floating">
                    <input v-model="email" type="email" class="form-control" placeholder="name@example.com" />
                    <label>Email address</label>
                </div>

                <div class="form-floating">
                    <input v-model="password" type="password" class="form-control" placeholder="Password" />
                    <label>Password</label>
                </div>

                <div class="form-floating">
                    <input
                        v-model="password_confirm"
                        type="password"
                        class="form-control"
                        placeholder="Password Confirm"
                    />
                    <label>Password Confirm</label>
                </div>
                <div class="form-floating">
                    <!-- <select v-model="user_type" name="user_type" size="3">
                        <option value="1">Banker</option>
                        <option value="2">Customer</option>
                        <option value="3">Funder</option>
                    </select> -->
                    <v-select v-model="user_type" :items="items" label="User type" data-vv-name="select" required>
                    </v-select>
                </div>
                <button v-if="!loading" class="w-100 btn btn-lg btn-primary" type="submit" :disabled="loading">
                    Submit
                </button>
                <semipolar-spinner v-if="loading" :animation-duration="2000" :size="65" color="#ff1d5e" />
            </form>
        </main>
    </v-app>
</template>

<script>
import axios from "axios";
import { SemipolarSpinner } from "epic-spinners";

export default {
    name: "Register",
    components: {
        SemipolarSpinner,
    },
    data() {
        return {
            user_name: "",
            email: "",
            password: "",
            password_confirm: "",
            user_type: "",
            loading: false,
            items: ["Banker", "Customer", "Funder"],
        };
    },
    methods: {
        submit() {
            this.loading = true;
            const USERTYPES = {
                Banker: 1,
                Customer: 2,
                Funder: 3,
            };
            const registerRequest = {
                method: "post",
                url: "api/v1/dj-rest-auth/registration/",
                data: {
                    username: this.user_name,
                    email: this.email,
                    password1: this.password,
                    password2: this.password_confirm,
                    user_type: Number(USERTYPES[this.user_type]),
                },
            };
            axios(registerRequest)
                .then((res) => {
                    this.$toast.success("Successfully created");
                    this.$router.push("/login");
                })
                .catch((error) => {
                    console.log(error);
                    this.$toast.error("Error creating account");
                });
            this.loading = false;
        },
    },
};
</script>

<style scoped>
.form-signin {
    width: 100%;
    max-width: 330px;
    padding: 15px;
    margin: auto;
}

.form-signin .checkbox {
    font-weight: 400;
}

.form-signin .form-floating:focus-within {
    z-index: 2;
}

.form-signin input[type="email"] {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}
</style>
