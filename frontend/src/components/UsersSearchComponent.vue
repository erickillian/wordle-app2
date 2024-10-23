<template>
    <SearchTable :headers="headers" :items="items" :search-query="searchQuery" item-key="slug"
        item-display-field="display_name" search-label="Search Users" search-icon="mdi-account-search-outline"
        item-name-plural="users" :selected-item="selectedUserSlug" :error="error" :loading="loading" :page="page"
        @item-selected="selectUser" @update:page="onPageUpdate" />
</template>

<script>
import { defineComponent } from 'vue';
import { fetchUsers } from '@/api/users';
import { usePaginatedSearch } from '@/composables/usePaginatedSearch';
import SearchTable from '@/components/SearchTable.vue';

export default defineComponent({
    name: 'UsersSearchComponent',
    props: {
        selectedUserSlug: {
            type: String,
            required: true,
        },
        onUserSelected: {
            type: Function,
            required: false,
        },
    },
    setup(props) {
        const { searchQuery, items, loading, error, page, onPageUpdate } = usePaginatedSearch(fetchUsers);

        const headers = [{ title: 'User', value: 'display_name' }];

        const selectUser = (slug) => {
            const newSlug = props.selectedUserSlug === slug ? '' : slug;
            props.onUserSelected?.(newSlug);
        };

        const onSearchQueryUpdate = (newQuery) => {
            searchQuery.value = newQuery;
        };

        return {
            headers,
            items,
            loading,
            error,
            page,
            selectUser,
            onPageUpdate,
            searchQuery,
            onSearchQueryUpdate,
        };
    },
});
</script>
