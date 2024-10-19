<template>
    <v-container class="fill-height d-flex justify-center align-center">
        <v-row justify="center">
            <v-col cols="12" sm="12" md="8" lg="6" xl="4" xxl="3">
                <v-card class="pa-4">
                    <v-btn icon @click="goBack" class="mr-2" elevation="0">
                        <v-icon>mdi-arrow-left</v-icon>
                    </v-btn>
                    <v-card-title class="d-flex justify-center align-center">
                        <span class="text-center">Login</span>
                    </v-card-title>
                    <v-card-text>
                        <v-form ref="loginForm" @keyup.enter="login">
                            <v-text-field v-model="email" label="Email" required :error-messages="error?.email"
                                type="email"></v-text-field>

                            <v-text-field v-model="password" label="Password" required :error-messages="error?.password"
                                type="password" autocomplete="password" ></v-text-field>

                            <!-- Display error message -->
                            <v-alert v-if="error?.error" type="error" dismissible>{{ error.error }}</v-alert>

                            <v-btn :disabled="loading" color="primary" block class="mt-1"
                                @click="login">
                                <v-progress-circular v-if="loading" indeterminate
                                    color="white"></v-progress-circular>
                                <span v-if="!loading">Login</span>
                            </v-btn>
                        </v-form>
                        <div class="mt-8">
                            <span>Don't have an account? <a @click="goToRegister" style="cursor: pointer; text-decoration: underline; color: var(--v-primary-base);">Register here</a></span>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useTheme } from 'vuetify';

export default defineComponent({
    name: 'LoginPage',
    setup() {
        const router = useRouter();
        const authStore = useAuthStore();
        const theme = useTheme();

        const email = ref('');
        const password = ref('');
        const error = ref({
            "email": '',
            "password": '',
            "error": '',
        });
        const loading = ref(false);

        const login = async () => {
            loading.value = true;
            error.value = { email: '', password: '', error: '' }; // Reset error before login attempt

            try {
                await authStore.login(email.value, password.value);
                router.push('/profile'); // Redirect to a different page after login
                // set the theme based on the user's color mode
                theme.global.name.value = authStore.user?.color_mode || 'system';

            } catch (err: any) {
                if (err.response && err.response.data) {
                    // Handle structured validation errors
                    error.value = {
                        ...error.value,
                        ...err.response.data
                    };
                } else {
                    // Handle general errors (e.g., network issues)
                    error.value = {
                        email: '',
                        password: '',
                        error: 'An unknown error occurred. Please try again.'
                    };
                }
            } finally {
                loading.value = false;
            }
        };

        const goBack = () => {
            router.push("/");
        };

        const goToRegister = () => {
            router.push("/register");
        };

        return {
            email,
            password,
            loading,
            error,
            login,
            goBack,
            goToRegister,
        };
    },
});
</script>

<style scoped>
.fill-height {
    height: 100vh;
}
</style>
