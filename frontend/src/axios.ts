import axios from 'axios';
import { useAuthStore } from './stores/auth';

const api = axios.create({
    baseURL: 'http://localhost:8000/', // Update with your API base URL
});

// Add a request interceptor
api.interceptors.request.use((config) => {
    const authStore = useAuthStore();
    if (authStore.accessToken) {
        config.headers.Authorization = `Bearer ${authStore.accessToken}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export default api;
