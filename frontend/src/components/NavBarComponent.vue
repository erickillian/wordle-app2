<template>
    <div>
        <v-app-bar dense app extended extension-height="0" :elevation="0" :clipped-left="true">
            <v-toolbar-title>Wordle</v-toolbar-title>
            <v-spacer></v-spacer>

            <!-- Mobile Menu Toggle (visible only on small screens) -->
            <v-btn icon @click="toggleDrawer" class="d-md-none">
                <v-icon>mdi-menu</v-icon>
            </v-btn>

            <!-- Desktop Menu Items (visible only on large screens) -->
            <v-toolbar-items class="d-none d-md-flex">
                <v-btn v-for="item in menuItems" :key="item.icon" :to="item.link" :href="item.link"
                    :class="{ 'v-btn--active': isActiveRoute(item.link) }">
                    <v-icon :left="true">{{ item.icon }}</v-icon>
                    {{ item.text }}
                </v-btn>
            </v-toolbar-items>
            <!-- <v-progress-linear active="isLoading" :indeterminate="true" class="ma-0" slot="extension" /> -->
        </v-app-bar>

        <!-- Mobile Drawer (visible only on small screens) -->
        <v-navigation-drawer v-model="drawer" absolute persistent touchless location="top">
            <v-list>
                <!-- List Items with Icon and Title -->
                <v-list-item v-for="(item, i) in menuItems" :key="i" @click="navigate(item.link)" color="primary"
                    :active="isActiveRoute(item.link)">
                    <template v-slot:prepend>
                        <v-icon :icon="item.icon"></v-icon>
                    </template>
                    <v-list-item-title>{{ item.text }}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useDisplay } from 'vuetify'; // Use Vuetify display helper


export default defineComponent({
  setup() {
    const store = useAuthStore(); // Use the auth store
    const router = useRouter();
    const isLoading = ref(false); // Loading state
    const drawer = ref(false); // Drawer open/close state
    const { mdAndDown } = useDisplay(); // Use Vuetify's display helper

    // Menu items with icons and links
    const menuItems = [
      { text: 'Dashboard', icon: 'mdi-view-dashboard', link: '/dashboard' },
      { text: 'Users', icon: 'mdi-account-group', link: '/users' },
      { text: 'Wordle', icon: 'mdi-alpha-w-box-outline', link: '/wordle' },
      { text: 'Profile', icon: 'mdi-account', link: '/profile' },
      { text: 'Logout', icon: 'mdi-logout', link: '/logout' },
    ];

    // watch the auth store for apiRequestLoading and update the isLoading ref
    watch(() => store.apiRequestLoading, (newVal) => {
        console.log(newVal);
        isLoading.value = newVal;
    });

    // Computed property for controlling drawer based on screen size
    const drawerState = computed(() => mdAndDown.value ? drawer.value : false);

    // Toggle drawer visibility
    const toggleDrawer = () => {
        if (mdAndDown.value) {
            drawer.value = !drawer.value; // Toggle only on mobile
        }
    };

    // Navigate function that closes the drawer after navigating
    const navigate = (link: string) => {
      router.push(link);
      drawer.value = false; // Close drawer after clicking on a menu item
    };

    // Check if the current route matches the base route or any of its subroutes
    const isActiveRoute = (link: string) => {
        return router.currentRoute.value.path.startsWith(link);
    };

    return {
      drawer: drawerState,
      menuItems,
      navigate,
      isActiveRoute,
      toggleDrawer,
    };
  },
});
</script>

<style scoped>
/* Optional: Custom styles */
</style>
