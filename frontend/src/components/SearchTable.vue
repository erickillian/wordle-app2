<template>
    <v-card class="pa-4" style="overflow-y: auto;" elevation="0">
        <v-card-title>
            <v-text-field v-model="searchQuery" :append-icon="searchIcon" :label="searchLabel" dense outlined
                single-line hide-details @input="onSearchInput" />
        </v-card-title>
        <v-card-text>
            <v-alert v-if="error" type="error" dismissible>
                Error Loading {{ itemNamePlural }}
            </v-alert>
            <v-data-table-server v-else :headers="headers" :items="items" :items-length="items.length"
                :item-key="itemKey" dense class="elevation-0" :loading="loading" hover @click:row="selectItem"
                hide-default-footer>
                <template v-slot:item="{ item }">
                    <tr :class="['data-table-row-search', { 'highlighted-row-light': !isDarkTheme && selectedItem === item[itemKey], 'highlighted-row-dark': isDarkTheme && selectedItem === item[itemKey] } ]"
                        @click="() => selectItem(item)" v-ripple style="cursor: pointer;">
                        <td>{{ item[itemDisplayField] }}</td>
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
                            No {{ itemNamePlural }} found.
                        </v-alert>
                    </div>
                </template>
            </v-data-table-server>
        </v-card-text>
    </v-card>
</template>

<script>
import { defineComponent } from 'vue';
import { useTheme } from 'vuetify';

export default defineComponent({
    name: 'SearchTable',
    props: {
        headers: {
            type: Array,
            required: true,
        },
        items: {
            type: Array,
            required: true,
        },
        itemKey: {
            type: String,
            required: true,
        },
        itemDisplayField: {
            type: String,
            required: true,
        },
        searchLabel: {
            type: String,
            required: true,
        },
        searchIcon: {
            type: String,
            default: 'mdi-magnify',
        },
        itemNamePlural: {
            type: String,
            required: true,
        },
        selectedItem: {
            type: [String, Number],
            required: false,
            default: null,
        },
        error: {
            type: Boolean,
            default: false,
        },
        loading: {
            type: Boolean,
            default: false,
        },
        page: {
            type: Object,
            required: true,
        },
        searchQuery: {
            type: String,
            required: true,
        },
    },
    emits: ['item-selected', 'update:search-query', 'update:page'],
    setup(props, { emit }) {
        const selectItem = (item) => {
            const itemKey = item[props.itemKey];
            const newItem = props.selectedItem === itemKey ? null : itemKey;
            emit('item-selected', newItem);
        };
        const isDarkTheme = useTheme().current.value.dark;

        const onSearchInput = (event) => {
            emit('update:search-query', event.target.value); // Use the input's value, not the event object.
        };

        const onPageUpdate = (newPage) => {
            emit('update:page', newPage); // Emit the updated page number
        };

        return {
            selectItem,
            onSearchInput,
            onPageUpdate,
            isDarkTheme,
        };
    },
});
</script>

<style scoped>
.data-table-row-search {
    transition: background-color 0.3s ease;
}

.highlighted-row-light {
    background-color: rgba(0, 0, 0, 0.1);
    /* Darken the row in light mode */
}

.highlighted-row-dark {
    background-color: rgba(255, 255, 255, 0.1);
    /* Lighten the row in dark mode */
}


</style>