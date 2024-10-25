import { defineStore } from 'pinia';
import { login as apiLogin, register as apiRegister, refresh as apiRefresh, getUserInfo, editUserInfo, logout } from '../api/auth';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: {
            email: "",
            full_name: "",
            display_name: "",
            date_joined: "",
            color_mode: "system",
            profile_picture: "",    
        },
        user_loading: false,
        user_error: null,
        login_error: null,
        accessToken: "",
        refreshToken: "",
        refreshTokenCreatedAt: "",
        apiRequestLoading: false,
    }),
    actions: {
        async editUserInfo(user: {}) {
            this.user_loading = true;
            try {
                const response = await editUserInfo(user);
                this.user = response.data;
            } catch (error) {
                console.error('Failed to edit user info:', error);
            } finally {
                this.user_loading = false;
            }
        },
        async fetchUserInfo() {
            this.user_loading = true;
            try {
                const response = await getUserInfo();
                this.user = response.data;
            } catch (error: any) {
                this.user_error = error.response.data;
            } finally {
                this.user_loading = false;
            }
        },
        async login(email: string, password: string) {
            try {
                const response = await apiLogin(email, password);
                this.accessToken = response.data.access;
                this.refreshToken = response.data.refresh;
                this.refreshTokenCreatedAt = response.data.created_at;
                this.user = response.data.user;
            } catch (error) {
                throw error;
            }
        },
        async register(email: string, password: string, hcaptcha: string) {
            try {
                const response = await apiRegister(email, password, hcaptcha);
                this.accessToken = response.data.access;
                this.refreshToken = response.data.refresh;
                this.refreshTokenCreatedAt = response.data.created_at;
                this.user = response.data.user;
            } catch (error) {
                throw error;
            }
        },
        async logout() {
            try {
                await logout(this.refreshToken);
            } catch (error) {
                console.error('Failed to logout:', error);
            } finally {
                this.$reset(); // Reset the store to its initial state
            }
        },
        async refresh() {
            if (!this.refreshToken) throw new Error('No refresh token available');

            try {
                const response = await apiRefresh(this.refreshToken);
                this.accessToken = response.data.access;
                this.refreshToken = response.data.refresh;
                return this.accessToken;
            } catch (error) {
                console.error('Failed to refresh token:', error);
                this.logout();
                throw error;
            }
        },
        async setApiRequestLoading(loading: boolean) {
            this.apiRequestLoading = loading;
        },
    },
    getters: {
        isAuthenticated: (state) => !!state.accessToken,
        getAccessToken: (state) => state.accessToken,
    },
    persist: true,
});
