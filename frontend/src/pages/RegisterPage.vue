<template>
    <v-container class="fill-height d-flex justify-center align-center">
        <v-row justify="center">
            <v-col cols="12" sm="12" md="8" lg="6" xl="4" xxl="3">
                <v-card class="pa-4">
                    <v-btn icon @click="goBack" class="mr-2" elevation="0">
                        <v-icon>mdi-arrow-left</v-icon>
                    </v-btn>
                    <v-card-title class="d-flex justify-center align-center">
                        <span class="text-center">Register</span>
                    </v-card-title>
                    <v-card-text>
                        <v-form ref="loginForm" @keyup.enter="register">
                            <v-text-field v-model="email" label="Email" required :error-messages="error?.email"
                                type="email"></v-text-field>

                            <v-text-field v-model="password1" label="Password" required
                                :error-messages="error?.password" type="password"
                                autocomplete="new-password"></v-text-field>

                            <v-text-field v-model="password2" label="Confirm Password" required type="password"
                                autocomplete="new-password" :error-messages="error?.password2"></v-text-field>

                            <div v-if="siteKey" id="h-captcha" class="h-captcha d-flex justify-center align-center"
                                :data-sitekey="siteKey"></div>

                            <!-- Display error message -->
                            <v-alert v-if="error?.non_field_errors" type="error" dismissible>{{
                                error.non_field_errors[0] }}</v-alert>

                            <v-btn :disabled="loading" color="primary" block class="mt-4" @click="register">
                                <v-progress-circular v-if="loading" indeterminate></v-progress-circular>
                                <span v-if="!loading">Register</span>
                            </v-btn>
                        </v-form>
                        <div class="mt-8">
                            <span>Already have an account? <a @click="goToLogin"
                                    style="cursor: pointer; text-decoration: underline; color: var(--v-primary-base);">Login
                                    here</a></span>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useTheme } from 'vuetify';

export default defineComponent({
    name: 'RegisterPage',
    setup() {
        const router = useRouter();
        const authStore = useAuthStore();
        const theme = useTheme();

        const email = ref('');
        const password1 = ref('');
        const password2 = ref('');
        const hcaptcha = ref('invalid_key');
        const siteKey = process.env.HCAPTCHA_SITE_KEY;
        const error = ref({
            email: '',
            password: '',
            password2: '',
            error: '',
            non_field_errors: '',
        });
        const loading = ref(false);

        const register = async () => {
            loading.value = true;
            error.value = { email: '', password: '', password2: '', non_field_errors: '', error: '' }; // Reset error before registration attempt

            // Check if passwords match
            if (password1.value !== password2.value) {
                error.value.password2 = 'Passwords do not match.';
                loading.value = false; // Stop loading as we have an error
                return;
            }

            try {
                await authStore.register(email.value, password1.value, hcaptcha.value);
                router.push('/dashboard'); // Redirect to a different page after registration
                // Set the theme based on the user's color mode
                theme.global.name.value = authStore.user?.color_mode || 'system';

            } catch (err) {
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
                        password2: '',
                        error: 'An unknown error occurred. Please try again.',
                        non_field_errors: '',
                    };
                }
            } finally {
                loading.value = false;
            }
        };

        const goBack = () => {
            router.push("/");
        };

        const goToLogin = () => {
            router.push("/login");
        };

        onMounted(() => {
            if (siteKey !== '') {
                const script = document.createElement('script');
                script.src = 'https://hcaptcha.com/1/api.js';
                script.async = true;
                script.defer = true;

                script.onload = () => {
                    if (window.hcaptcha) {
                    window.hcaptcha.render('h-captcha', {
                        sitekey: siteKey,
                        size: 'normal',  // Can also be 'compact' if you want a smaller widget
                        callback: (response) => {
                        console.log('hCaptcha completed:', response);  // Handle the response
                        hcaptcha.value = response;
                        },
                        'error-callback': (error) => {
                        console.error('hCaptcha error:', error);
                        }
                    });
                    } else {
                    console.error("hCaptcha failed to load.");
                    }
                };

                document.head.appendChild(script);
            }
        });

        return {
            email,
            password1,
            password2,
            loading,
            error,
            siteKey,
            register,
            goBack,
            goToLogin,
        };
    },
});
</script>

<style scoped>
.fill-height {
    height: 100vh;
}
</style>
