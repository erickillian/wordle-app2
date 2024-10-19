<template>
    <v-container class="fill-height d-flex justify-center align-center">
        <v-row justify="center">
            <v-col cols="12" class="text-center">
                <v-progress-circular
                    v-if="loading"
                    indeterminate
                    color="primary"
                    size="64"
                ></v-progress-circular>
                <div v-else>
                    <h1>Logging out...</h1>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useTheme } from 'vuetify';

export default defineComponent({
    name: 'LogoutPage',
    setup() {
        const theme = useTheme();
        const router = useRouter();
        const authStore = useAuthStore();
        const loading = ref(true);

        const logout = async () => {
            try {
                await authStore.logout();
                router.push('/'); // Redirect to home page after logout
                theme.global.name.value = 'system'; // Reset theme to system theme
            } catch (error) {
                console.error('Logout failed:', error);
            } finally {
                loading.value = false;
            }
        };

        onMounted(() => {
            logout(); // Call logout when the component is mounted
        });

        return {
            loading,
        };
    },
});
</script>

<style scoped>
.fill-height {
    height: 100vh;
}
.text-center {
    text-align: center;
}
</style>
