<template>
    <v-card class="pa-4" style="overflow-y: auto;" elevation="0">
        <v-card-title>
            <v-text-field v-model="searchQuery" append-icon="mdi-magnify" label="Search Words" dense outlined
                single-line hide-details />
        </v-card-title>
        <v-card-text>
            <v-alert v-if="error" type="error" dismissible>
                Error Loading Words
            </v-alert>
            <v-data-table-server v-else :headers="headers" :items="items" :items-length="items.length" item-key="word"
                dense class="elevation-0" :loading="loading" hover @click:row="selectWord" hide-default-footer>
                <template v-slot:item="{ item }">
                    <tr :class="{ 'highlighted-row': selectedWord === item.word }" @click="() => selectWord(item)"
                        style="cursor: pointer;">
                        <td>{{ item.word }}</td>
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
                            No words found.
                        </v-alert>
                    </div>
                </template>
            </v-data-table-server>
        </v-card-text>
    </v-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { usePaginatedSearch } from "@/composables/usePaginatedSearch";
import { words as fetchWords } from "@/api/wordle";

export default defineComponent({
    name: "WordsSearchComponent",
    props: {
        selectedWord: {
            type: String,
            required: false,
            default: null,
        },
        onWordSelected: {
            type: Function,
            required: false,
        },
    },
    setup(props) {
        const {
            searchQuery,
            items,
            loading,
            error,
            page,
            onPageUpdate,
        } = usePaginatedSearch(fetchWords);

        const headers = [
            { title: "Word", value: "word" },
        ];

        const selectWord = (item) => {
            const word = item.word;
            const newWord = (props.selectedWord === word) ? null : word;
            props.onWordSelected?.(newWord);
        };

        return {
            searchQuery,
            items,
            loading,
            error,
            page,
            selectWord,
            headers,
            onPageUpdate,
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
