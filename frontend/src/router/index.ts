import { createRouter, createWebHistory } from 'vue-router/auto';
import { setupLayouts } from 'virtual:generated-layouts';
import { useAuthStore } from '@/stores/auth'; // Import the Pinia auth store
import { storeToRefs } from 'pinia'; // For extracting store state in reactive form

const publicRoutes = [
    {
        path: '/',
        component: () => import('@/pages/HomePage.vue'), // Homepage component
    },
    {
        path: '/login',
        component: () => import('@/pages/LoginPage.vue'), // Login component
    },
    {
        path: '/register',
        component: () => import('@/pages/RegisterPage.vue'), // Register component
    },
];

// Internal routes wrapped in InternalLayout, except for logout
const internalRoutes = [
    {
        path: '/logout',
        component: () => import('@/pages/LogoutPage.vue'), // Logout component
        meta: { requiresAuth: true },
    },
    {
        path: '/',
        component: () => import('@/layouts/InternalLayout.vue'), // Internal layout with app bar
        meta: { requiresAuth: true },
        children: [
            {
                path: 'profile',
                component: () => import('@/pages/ProfilePage.vue'), // Profile page
                meta: { requiresAuth: true },
            },
            {
                path: 'dashboard',
                component: () => import('@/pages/DashboardPage.vue'), // Dashboard page
                meta: { requiresAuth: true },
            },
            {
                path: 'users',
                component: () => import('@/pages/UsersPage.vue'), // Users page
                meta: { requiresAuth: true },
            },
            {
                path: 'users/:slug',
                component: () => import('@/pages/UsersPage.vue'), // Users page with slug
                meta: { requiresAuth: true },
                props: (route: { params: { slug: string } }) => ({ slug: route.params.slug }), // Pass slug as a prop
            },
            {
                path: 'wordle',
                component: () => import('@/pages/WordlePage.vue'), // Wordle page
                meta: { requiresAuth: true },
            },
            {
                path: 'wordle/:slug',
                component: () => import('@/pages/WordlePage.vue'), // Wordle page
                meta: { requiresAuth: true },
                props: (route: { params: { slug: string } }) => ({ slug: route.params.slug }), // Pass slug as a prop
            },
            {
                path: 'words',
                component: () => import('@/pages/WordPage.vue'), // Word page
                meta: { requiresAuth: true },
            },
            {
                path: 'words/:word',
                component: () => import('@/pages/WordPage.vue'), // Word page with word parameter
                meta: { requiresAuth: true },
                props: (route: { params: { word: string } }) => ({ word: route.params.word }), // Pass word as a prop
            },
            // Add more internal pages here
        ],
    },
];

// Merge public and internal routes
const extendedRoutes = setupLayouts([
    ...publicRoutes,
    ...internalRoutes,
    {
        path: '/:pathMatch(.*)*',
        redirect: '/login', // Redirect to login for undefined paths
    },
]);

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: extendedRoutes,
});

// Global navigation guard to check if user is logged in using the store
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore(); // Access the auth store
    const { accessToken } = storeToRefs(authStore); // Extract access token reactively

    const loggedIn = !!accessToken.value; // Check if user is logged in based on the store's state

    // If route requires authentication and user is not logged in
    if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
        next({ path: '/login' });
    }
    // If user is logged in and trying to access public routes
    else if (loggedIn && publicRoutes.some(route => route.path === to.path)) {
        next({ path: '/profile' }); // Redirect to a default internal page
    }
    // // If user is not logged in and trying to access internal routes
    // else if (!loggedIn && internalRoutes.some(route => route.path === to.path)) {
    //     next({ path: '/login' });
    // }
    // Proceed to the route
    else {
        next();
    }
});

// Workaround for dynamic import errors
router.onError((err, to) => {
    if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
        if (!localStorage.getItem('vuetify:dynamic-reload')) {
            console.log('Reloading page to fix dynamic import error');
            localStorage.setItem('vuetify:dynamic-reload', 'true');
            location.assign(to.fullPath);
        } else {
            console.error('Dynamic import error, reloading page did not fix it', err);
        }
    } else {
        console.error(err);
    }
});

router.isReady().then(() => {
    localStorage.removeItem('vuetify:dynamic-reload');
});

export default router;
