<template>
    <v-app>
        <main class="form-signin">
            <form @submit.prevent="submit">
                <h1 class="h3 mb-3 fw-normal">Sign in</h1>

                <div class="form-floating">
                    <input
                        v-model="user_name"
                        type=""
                        class="form-control"
                        placeholder="Username"
                    />
                    <label>Username</label>
                </div>
                <div class="form-floating">
                    <input
                        v-model="password"
                        type="password"
                        class="form-control"
                        placeholder="Password"
                    />
                    <label>Password</label>
                </div>

                <button class="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
                <router-link to="/register" class="nav-link" active-class="active">
                    Don't have an account? Register Here!
                </router-link>
            </form>
        </main>
    </v-app>
</template>

<script>
import axios from 'axios';
import { User } from '../models/User';

export default {
    name: 'Login',
    data() {
        return {
            user_name: '',
            password: '',
            user: new User(),
        };
    },
    methods: {
        submit() {
            const loginRequest = {
                method: 'post',
                url: 'api/v1/dj-rest-auth/login/',
                data: {
                    username: this.user_name,
                    password: this.password,
                },
            };
            axios(loginRequest, { withCredentials: true })
                .then((res) => {
                    localStorage.setItem('username', this.user_name);
                    localStorage.setItem('token', res.data.key);
                    this.getUserInfo();
                })
                .catch((error) => {
                    console.log(error);
                    this.$toast.error('Error logging in.');
                });
        },
        async getUserInfo() {
            const username = localStorage.getItem('username');
            const token = localStorage.getItem('token');

            const userProfile = {
                method: 'get',
                url: `users/${username}/`,
                headers: {
                    Authorization: `Token ${token}`,
                },
            };

            try {
                let { data } = await axios(userProfile);
                this.user.id = data.pk;
                this.user.username = data.username;
                this.user.email = data.email;
                this.user.user_type = data.user_type;
                localStorage.setItem('user', JSON.stringify(this.user));

                if (this.user.user_type == 1) {
                    this.$router.push('/banker');
                } else if (this.user.user_type == 2) {
                    this.$router.push('/customer');
                } else if (this.user.user_type == 3) {
                    this.$router.push('/funder');
                }
            } catch (error) {
                console.log(error);
                this.$toast.error('Error while getting user data.');
                await this.$router.push('/login');
            }
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

.form-signin input[type='email'] {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
}

.form-signin input[type='password'] {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}
</style>
