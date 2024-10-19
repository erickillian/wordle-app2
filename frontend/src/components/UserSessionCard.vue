<template>
    <div class="user-session-card">
        <v-card class="mb-5">
            <v-card-title class="py-4 font-weight-bold">
                Active Sessions
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-6">
                <v-row>
                    <v-col cols="12">
                        <!-- Check if userSessions exist -->
                        <v-list v-if="userSessions.length" class="sessions-list">
                            <v-list-item v-for="session in userSessions" :key="session.id" class="session-item"
                                :class="{ 'session-item-sm': $vuetify.display.smAndDown }">
                                <v-row justify="space-between" class="mb-4">
                                    <v-col cols="12" md="6">
                                        <v-list-item-title class="font-weight-bold text-h6">
                                            {{ session.device }}
                                        </v-list-item-title>
                                    </v-col>

                                    <v-col cols="12" md="6">
                                        <v-list-item-action class="d-flex align-center justify-space-between">
                                            <div>
                                                <strong>Created:</strong> {{ new
                                                Date(session.created_at).toLocaleString() }}
                                            </div>
                                            <div>
                                                <strong>Expires:</strong> {{ new
                                                Date(session.expires_at).toLocaleString() }}
                                            </div>
                                        </v-list-item-action>
                                    </v-col>
                                </v-row>

                                <v-row justify="space-between">
                                    <v-col cols="12" md="6">
                                        <div>
                                            <strong>IP Address:</strong> {{ session.ip_address }}
                                        </div>
                                    </v-col>
                                    <v-col cols="12" md="6">
                                        <div>
                                            <strong>Location:</strong> {{ session.location }}
                                        </div>
                                    </v-col>
                                    <v-col cols="12" class="d-flex justify-end">
                                        <v-btn icon @click="handleRemoveSession(session.created_at)" elevation="0">
                                            <v-icon color="error">mdi-close</v-icon>
                                        </v-btn>
                                    </v-col>
                                </v-row>

                                <v-divider class="my-4"></v-divider>
                            </v-list-item>
                        </v-list>

                        <!-- Show skeleton loader when loading -->
                        <v-skeleton-loader v-else :loading="userSessionsLoading" type="list-item"></v-skeleton-loader>
                    </v-col>
                </v-row>
            </v-card-text>

            <div class="d-flex justify-center py-4 align-center" v-if="page ? page.total_pages > 1 : false">
                <v-pagination v-model="page.current_page" :length="page ? page.total_pages : 0"
                    :total-visible="page.page_size" size="small" aria-label="Pagination"
                    @update:model-value="paginate"></v-pagination>
            </div>
        </v-card>
    </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { getUserSessions, removeSession as apiRemoveSession } from '@/api/auth'; // Renamed import

export default {
    name: 'UserSessionCard',
    setup() {
        const userSessions = ref([]);
        const page = ref({
            page_size: 10,
            total_pages: 0,
            current_page: 1,
            count: 0,
            has_next: false,
            has_prev: false,
        });
        const userSessionsLoading = ref(false);

        // Fetch the sessions from the API
        const fetchActiveTokens = async (currentPage = 1) => {
            userSessionsLoading.value = true;
            try {
                const response = await getUserSessions(currentPage);
                userSessions.value = response.data.results;
                // Update page data from API response
                page.value = {
                    ...page.value,
                    current_page: response.data.page.current_page,
                    total_pages: response.data.page.total_pages,
                    count: response.data.page.count,
                    has_next: response.data.page.has_next,
                    has_prev: response.data.page.has_prev,
                };
            } catch (error) {
                console.error('Error fetching active tokens:', error);
            } finally {
                userSessionsLoading.value = false;
            }
        };

        // Renamed this method to avoid recursion
        const handleRemoveSession = async (created_at) => {
            console.log('Remove session:', created_at);
            try {
                await apiRemoveSession(created_at); // Call the API function
                let new_page = page.value.current_page;
                if (userSessions.value.length === 1 && new_page > 1) {
                    new_page -= 1;
                }
                fetchActiveTokens(new_page);
            } catch (error) {
                console.error('Error removing session:', error);
            }
        };

        const paginate = (newPage) => {
            page.value.current_page = newPage; // Update the current page
            fetchActiveTokens(newPage);
        };

        // Fetch the first page of tokens when the component mounts
        onMounted(() => {
            fetchActiveTokens(page.value.current_page);
        });

        return {
            page,
            userSessions,
            userSessionsLoading,
            paginate,
            handleRemoveSession, // Updated to reflect new method name
        };
    },
};
</script>

<style scoped></style>
