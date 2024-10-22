<template>
    <v-card class="pa-4" style="overflow-y: auto;" elevation="0">
        <v-card-title>
            <v-text-field v-model="searchQuery" append-icon="mdi-account-search-outline" label="Search Users" dense
                outlined single-line hide-details />
        </v-card-title>
        <v-card-text>
            <v-alert v-if="error" type="error" dismissible>
                Error Loading Users
            </v-alert>
            <v-data-table-server v-else :headers="headers" :items="items" :items-length="items.length" item-key="slug" dense class="elevation-0"
                :loading="loading" hover @click:row="selectUser" hide-default-footer>
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

<script>
import { defineComponent } from "vue";
import { fetchUsers } from "@/api/users";
import { usePaginatedSearch } from "@/composables/usePaginatedSearch";

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
        const { searchQuery, items, loading, error, page, onPageUpdate } = usePaginatedSearch(fetchUsers);

        // Select user and notify parent component
        const selectUser = (item) => {
            const user_slug = item.slug;
            const newSlug = (props.selectedUserSlug === user_slug) ? '' : user_slug;
            props.onUserSelected?.(newSlug);
        };

        // // Watch for prop change
        // watch(() => props.selectedUserSlug, (slug) => {
        //     // Ensure selected user slug updates properly
        // });

        return {
            searchQuery, items, loading, error, page, selectUser, selectedUserSlug: props.selectedUserSlug, headers: [{ title: "User", value: "display_name" }], onPageUpdate,
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
