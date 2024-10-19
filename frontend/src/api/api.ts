import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

let BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";
const USE_HTTPS = process.env.USE_HTTPS || false;

if (USE_HTTPS) {
    if (!BACKEND_URL.startsWith('http://') && !BACKEND_URL.startsWith('https://')) {
        BACKEND_URL = 'https://' + BACKEND_URL;
    } else {
        BACKEND_URL = BACKEND_URL.replace('http://', 'https://');
    }
}

const api = axios.create({
    baseURL: BACKEND_URL, // Use BACKEND_URL if it exists, otherwise fallback to localhost
    timeout: 10000,
});



api.interceptors.request.use(
    config => {
        const authStore = useAuthStore();
        if (authStore.isAuthenticated && !config.url?.includes('/refresh')) {
            const token = authStore.getAccessToken;
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        }
        return config;
    },
    error => Promise.reject(error)
);

api.interceptors.response.use(
    response => response,
    async error => {
        const { response } = error;
        const authStore = useAuthStore();
        const config = error.config;

        // Prevent infinite retry loops by not retrying refresh/logout routes
        if (config.url?.includes('/refresh') || config.url?.includes('/logout')) {
            return Promise.reject(error);
        }

        // Attach a retry flag to each request, default to false
        if (!config._retry) {
            config._retry = 0; // Initialize retry counter for this specific request
        }

        if (response && response.status === 401 && config._retry < 3 && !config._isRetryRequest) { // Unauthorized and retry limit not reached
            config._isRetryRequest = true; // Mark this request as a retry request
            try {
                // Try to refresh the token
                const newAccessToken = await authStore.refresh();
                if (newAccessToken) {
                    config.headers.Authorization = `Bearer ${newAccessToken}`;
                    config._retry += 1; // Increment retry counter for this request
                    return api.request(config); // Retry the original request with the new token
                }
            } catch (refreshError) {
                authStore.logout();
            }
        }

        if (config._retry >= 3) {
            authStore.logout();
        }

        return Promise.reject(error);
    }
);

export default api;
