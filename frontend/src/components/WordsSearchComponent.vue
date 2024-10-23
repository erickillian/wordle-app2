<template>
    <SearchTable :headers="headers" :items="items" :search-query="searchQuery" item-key="word" item-display-field="word"
        search-label="Search Words" search-icon="mdi-magnify" item-name-plural="words" :selected-item="selectedWord"
        :error="error" :loading="loading" :page="page" @item-selected="selectWord" @update:page="onPageUpdate"
        @update:search-query="onSearchQueryUpdate" />
</template>

<script>
import { defineComponent } from 'vue';
import { usePaginatedSearch } from '@/composables/usePaginatedSearch';
import { words as fetchWords } from '@/api/wordle';
import SearchTable from '@/components/SearchTable.vue';

export default defineComponent({
    name: 'WordsSearchComponent',
    props: {
        selectedWord: {
            type: String,
            required: true,
        },
        onWordSelected: {
            type: Function,
            required: false,
        },
    },
    setup(props) {
        const { searchQuery, items, loading, error, page, onPageUpdate } = usePaginatedSearch(fetchWords);

        const headers = [{ title: 'Word', value: 'word' }];

        const selectWord = (word) => {
            const newWord = props.selectedWord === word ? null : word;
            props.onWordSelected?.(newWord);
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
            selectWord,
            onPageUpdate,
            searchQuery,
            onSearchQueryUpdate,
        };
    },
});
</script>
