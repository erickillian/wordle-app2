<template>
  <v-app>
    <NavBarComponent />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import NavBarComponent from '@/components/NavBarComponent.vue';

export default defineComponent({
    name: 'InternalLayout',
    components: {
        NavBarComponent,
    },
});
</script>

<style scoped>
/* Add styles if needed */
</style>
