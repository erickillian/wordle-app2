<template>
  <v-app>
    <NavBarComponent>
    </NavBarComponent>

    <v-main>
      <router-view /> <!-- Render the current route's component -->
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import NavBarComponent from '@/components/NavBarComponent.vue';

export default defineComponent({
    name: 'InternalLayout',
    components: {
        NavBarComponent,
    },
    setup() {
        const router = useRouter();

        const goToProfile = () => {
        router.push('/profile');
        };

        const logout = () => {
        router.push('/logout');
        };

        const goToDashboard = () => {
        router.push('/dashboard');
        };

        return {
        goToDashboard,  
        goToProfile,
        logout,
        };
    },
});
</script>

<style scoped>
/* Add styles if needed */
</style>
