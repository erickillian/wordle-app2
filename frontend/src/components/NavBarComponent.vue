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
                <v-list-item>
                    <!-- Dropdown Menu -->
                    <v-menu v-model="menuVisible" offset-y :close-on-content-click="false"
                        @click-outside="menuVisible = false">
                        <template v-slot:activator="{ props: activatorProps }">
                            <v-btn icon v-bind="activatorProps">
                                <v-img v-if="user?.profile_picture" :src="getProfilePictureUrl(user.profile_picture)"
                                    alt="Profile Picture" width="46" height="46" />
                            </v-btn>
                        </template>
                        <v-card rounded="lg" min-width="400">
                            <v-card-title class="d-flex flex-column align-items-center text-center">
                                <v-img v-if="user?.profile_picture" :src="getProfilePictureUrl(user.profile_picture)"
                                    alt="Profile Picture" width="100" height="100" class="mb-3 mx-auto" />
                                <div>
                                    <div>{{ user?.email }}</div>
                                </div>
                            </v-card-title>
                            <!-- <v-card-actions>
                                <v-btn text @click="navigate('/profile')" >Edit Profile</v-btn>
                            </v-card-actions> -->
                            <v-list>
                                <v-list-item v-for=" item in menuItems" :key="item.icon" @click="navigate(item.link)" :to="item.link">
                                    <template v-slot:prepend>
                                        <v-icon>{{ item.icon }}</v-icon>
                                    </template>
                                    <v-list-item-title>{{ item.text }}</v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-card>

                </v-menu>
                </v-list-item>
            </v-toolbar-items>


            <!-- <v-progress-linear active="isLoading" :indeterminate="true" class="ma-0" slot="extension" /> -->
        </v-app-bar>

        <!-- Mobile Drawer (visible only on small screens) -->
        <v-navigation-drawer v-model="drawer" absolute persistent location="top">
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

<script>
import { defineComponent, ref, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useDisplay } from 'vuetify'; // Use Vuetify display helper

export default defineComponent({
    setup() {
        const store = useAuthStore(); // Use the auth store
        const router = useRouter();
        const isLoading = ref(false); // Loading state
        const drawer = ref(false); // Drawer open/close state
        const { smAndDown } = useDisplay(); // Use Vuetify's display helper
        const user = store.user; // Get the user object from the store
        const menuVisible = ref(false); // Local state for menu visibility

        // Menu items with icons and links
        const menuItems = [
            { text: 'Dashboard', icon: 'mdi-view-dashboard', link: '/dashboard' },
            { text: 'Users', icon: 'mdi-account-group', link: '/users' },
            { text: 'Wordle', icon: 'mdi-alpha-w-box-outline', link: '/wordle' },
            { text: 'Dictionary', icon: 'mdi-book-open-page-variant', link: '/words' },
            { text: 'Edit Profile', icon: 'mdi-account', link: '/profile' },
            { text: 'Logout', icon: 'mdi-logout', link: '/logout' },
        ];

        // Watch the auth store for apiRequestLoading and update the isLoading ref
        watch(() => store.apiRequestLoading, (newVal) => {
            console.log(newVal);
            isLoading.value = newVal;
        });

        // Computed property for controlling drawer based on screen size
        const drawerState = computed(() => smAndDown.value ? drawer.value : false);

        // Toggle drawer visibility
        const toggleDrawer = () => {
            if (smAndDown.value) {
                drawer.value = !drawer.value; // Toggle only on mobile
            }
        };

        // Navigate function that closes the drawer after navigating
        const navigate = (link) => {
            router.push(link);
            drawer.value = false; // Close drawer after clicking on a menu item
            menuVisible.value = false; // Close the dropdown menu
        };

        // Check if the current route matches the base route or any of its subroutes
        const isActiveRoute = (link) => {
            return router.currentRoute.value.path.startsWith(link);
        };

        // Function to get the profile picture URL
        const getProfilePictureUrl = (picture_url) => {
            return `/static/profile_pictures/${picture_url}`;
        }

        return {
            drawer: drawerState,
            menuItems,
            user,
            menuVisible,
            navigate,
            isActiveRoute,
            toggleDrawer,
            getProfilePictureUrl,
        };
    },
});
</script>

<style scoped>
/* Optional: Custom styles */
</style>
