<template>
    <v-card>
        <v-card-text>
            <p class="text-h6">
                <v-icon left class="mr-2">{{ icon }}</v-icon>
                {{ title }}
            </p>

            <!-- Info Button -->
            <div style="position: absolute; top: 10px; right: 10px;">
                <v-btn icon @click="dialog = true" elevation="0">
                    <v-icon>mdi-information-outline</v-icon>
                </v-btn>
            </div>

            <!-- Info Dialog -->
            <v-dialog v-model="dialog" max-width="600px">
                <v-card>
                    <v-card-title>
                        <span class="text-h6">{{ title }}</span>
                    </v-card-title>
                    <v-card-text>
                        <slot></slot>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="primary" text @click="dialog = false">Close</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-card-text>

        <v-data-table-server :headers="getHeaders()" :items="items" class="elevation-0" hide-default-footer disable-sort
            hover @click:row="handleRowClick" :items-length="items.length" :loading="loading">
            <!-- if rankItems is turned on add a column that shows each players rank -->
            <template v-slot:[`item.rank`]="{ index, item }" v-if="rankItems">
                <v-list-item-title>
                    <v-icon v-if="index + 1 <= 3 && (page.current_page == 1)" :color="placeColors[index + 1]">
                        mdi-star-circle
                    </v-icon>
                    {{ (page.current_page - 1) * page.page_size + index + 1 }}
                </v-list-item-title>
            </template>

            <!-- User Full Name with Ranking Icons -->
            <template v-slot:[`item.user`]="{ index, item }">

                <div style="display: flex; align-items: center;">
                    <v-list-item-media>
                        <v-img :src="getProfilePictureUrl(item.user ? item.user.profile_picture : item.profile_picture)"
                            width="32" height="32" class="mr-2" />
                    </v-list-item-media>

                    <v-list-item-title>
                        <!-- <v-icon v-if="rankItems && (index + 1 <= 3) && (page.current_page == 1)"
                            :color="placeColors[index + 1]">
                            mdi-star-circle
                        </v-icon> -->
                        {{ item.user ? (item.user.display_name) : (item.display_name) }}
                    </v-list-item-title>
                </div>
            </template>

            <!-- Guesses with Chip Color -->
            <template v-slot:[`item.guesses`]="{ item }">
                <v-chip :color="getColor(item.solved)">
                    {{ item.guesses }}
                </v-chip>
            </template>

            <template v-slot:[`item.start_time`]="{ item }">
                <v-list-item-title>
                    {{ new Date(item.start_time).toLocaleDateString('en-US', { timeZone: 'UTC', year: 'numeric', month: 'long', day: 'numeric' }) }}
                </v-list-item-title>
            </template>

            <!-- Streak -->
            <template v-slot:[`item.streak`]="{ item }">
                <v-list-item-title v-if="item.streak >= 3">
                    <img v-if="item.streak >= 3" style="max-width: 20px; max-height: 20px" class="mr-3"
                        src="/streak.png" />
                    {{ item.streak }}
                </v-list-item-title>
            </template>

            <!-- Pagination -->
            <template v-slot:bottom>
                <div class="d-flex justify-center py-4 align-center" v-if="page ? page.total_pages > 1 : false">
                    <v-pagination v-model="page.current_page" :length="page ? page.total_pages : 0"
                        :total-visible="numPagination" size="small" aria-label="Pagination"
                        @update:model-value="onPageUpdate"></v-pagination>
                </div>
            </template>

            <!-- No Data -->
            <template v-slot:no-data>
                <div class="pa-4">
                    <v-alert :value="true" icon="mdi-information">
                        No data found.
                    </v-alert>
                </div>
            </template>
        </v-data-table-server>
    </v-card>
</template>

<script lang>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';


export default {
    props: {
        title: String,
        icon: String,
        items: Array,
        headers: Array,
        hide_footer: {
            type: Boolean,
            default: true
        },
        page: {
            type: Object,
            required: false,
            default: () => ({
                current_page: 1,
                page_size: 10,
                total_pages: 1,
                has_next: false,
                has_prev: false,
            }),
        },
        pageChange: {
            type: Function,
            required: false,
        },
        loading: {
            type: Boolean,
            default: false,
            required: false,
        },
        rankItems: {
            type: Boolean,
            default: false,
            required: false,
        },
        numPagination: {
            type: Number,
            default: 5,
            required: false,
        },
    },
    data() {
        return {
            dialog: false,  // State to control the dialog visibility
            placeColors: {
                1: "amber darken-3", // Gold
                2: "blue-grey lighten-5", // Silver
                3: "brown darken-2", // Bronze
            },
        };
    },
    setup(props) {
        const router = useRouter();

        const placeClasses = {
            1: "yellow--text text--accent-4",
            2: "blue-grey--text text--lighten-4",
            3: "brown--text text--darken-1",
        };

        const handleRowClick = (item, event) => {
            const rowItem = props.items[event.index];
            if (rowItem.user) {  // wordles have the user attribute but users do not as they are the user
                router.push(`/wordle/${rowItem.slug}`);
            } else {
                router.push(`/users/${rowItem.slug}`);
            }
        }

        const getColor = (solved) => {
            return solved ? "green" : "red";
        };

        const getHeaders = () => {
            let headers = [...props.headers];
            if (props.rankItems) {
                headers.unshift({
                    align: 'start',
                    key: 'rank',
                    title: 'Rank'
                });
            }
            return headers;
        };

        function getProfilePictureUrl(picture_url) {
            return `/static/profile_pictures/${picture_url}`;
        }

        const onPageUpdate = (newPage) => {
            props.pageChange(newPage);
        };

        return {
            handleRowClick,
            getColor,
            getHeaders,
            onPageUpdate,
            getProfilePictureUrl,
        };
    },
};
</script>

<style scoped></style>
