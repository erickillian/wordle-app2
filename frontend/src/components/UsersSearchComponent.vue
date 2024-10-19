<template>
    <v-card class="pa-4" style="overflow-y: auto;" elevation="0">
        <v-card-title>
            <v-text-field v-model="usersSearch" append-icon="mdi-account-search-outline" label="Search Users" dense
                outlined single-line hide-details />
        </v-card-title>
        <v-card-text>
            <v-alert v-if="error" type="error" dismissible>
                Error Loading Users
            </v-alert>
            <v-data-table-server v-else :headers="headers" :items="users" :items-length="users.length" item-key="slug" dense class="elevation-0"
                :loading="users_loading" hover @click:row="selectUser" hide-default-footer>
                <template v-slot:item="{ item }">
                    <tr :class="{ 'highlighted-row': selectedUserSlug === item.slug }" @click="() => selectUser(item)"
                        style="cursor: pointer;">
                        <td>{{ item.display_name }}</td>
                    </tr>
                </template>
                <template v-slot:bottom>
                    <div class="d-flex justify-center py-4 align-center">
                        <v-pagination v-model="page.current_page" :length="page.total_pages" :total-visible="5"
                            size="small" @update:model-value="onPageUpdate" />
                    </div>
                </template>
                <template v-slot:no-data>
                    <div class="pa-4">
                        <v-alert :value="true" icon="mdi-information">
                            No users found.
                        </v-alert>
                    </div>
                </template>
            </v-data-table-server>
        </v-card-text>
    </v-card>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch } from "vue";
import { fetchUsers } from "@/api/users";
import { User } from "@/types/index";

export default defineComponent({
    name: "UserListPage",
    props: {
        selectedUserSlug: {
            type: String,
            required: false,
            default: '',
        },
        onUserSelected: {
            type: Function,
            required: false,
        },
    },
    setup(props) {
        const usersSearch = ref("");
        const users = ref<User[]>([]);
        const users_loading = ref(false);
        const error = ref(false);

        const page = ref({
            current_page: 1,
            total_pages: 1,
            page_size: 20,
            count: 0,
            has_next: false,
            has_prev: false,
        });

        const headers = [
            { title: "User", value: "display_name" },
        ];

        // Fetch users based on search and page
        const getSearchUsers = async (search: string, page_num: number) => {
            users_loading.value = true;
            error.value = false;
            try {
                const response = await fetchUsers(search, page_num);
                users.value = response.data.results;
                page.value = {
                    current_page: response.data.page.current_page,
                    total_pages: response.data.page.total_pages,
                    page_size: response.data.page.page_size,
                    count: response.data.page.count,
                    has_next: response.data.page.has_next,
                    has_prev: response.data.page.has_prev,
                };
            } catch {
                error.value = true;
                users.value = [];
            } finally {
                users_loading.value = false;
            }
        };

        // Select user and notify parent component
        const selectUser = (item: User) => {
            const user_slug = item.slug;
            const newSlug = (props.selectedUserSlug === user_slug) ? '' : user_slug;
            props.onUserSelected?.(newSlug);
        };

        const onPageUpdate = (newPage: number) => {
            getSearchUsers(usersSearch.value, newPage);
        };

        // Watcher for search input changes
        watch(usersSearch, (newSearch) => {
            page.value.current_page = 1;
            getSearchUsers(newSearch, page.value.current_page);
        });

        // Watch for prop change
        watch(() => props.selectedUserSlug, (slug) => {
            // Ensure selected user slug updates properly
        });

        onMounted(() => {
            getSearchUsers(usersSearch.value, page.value.current_page);
        });

        return {
            usersSearch, users, users_loading, error, page, selectUser, selectedUserSlug: props.selectedUserSlug, headers, onPageUpdate,
        };
    },
});
</script>

<style scoped>
.highlighted-row {
    background-color: #ffffff33;
    transition: background-color 0.3s ease-in-out;
}
</style>
