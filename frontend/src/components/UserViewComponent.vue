<template>
    <v-card style="height: 100%">
        <v-card-title class="py-2">
            <v-row justify="center" class="my-0">
                <v-col cols="auto" class="text-center">
                    <v-img :src="getProfilePictureUrl(user.profile_picture)" width="100" height="100" 
                        style="max-width: 100%; height: auto;" />
                </v-col>
            </v-row>
            <v-row justify="center" class="my-0">
                <v-col cols="auto" class="text-center">
                    <h1 style="font-size: 2rem; text-align: center;">{{ user.display_name }}</h1>
                </v-col>
            </v-row>
        </v-card-title>

        <v-tabs v-model="activeTab" class="mt-3" grow color="primary">
            <v-tab v-for="(tab, index) in tabs" :key="index" :value="tab.value">
                <v-icon start>{{ tab.icon }}</v-icon>
                {{ tab.title }}
            </v-tab>
        </v-tabs>
        <v-tabs-window v-model="activeTab">
            <v-tabs-window-item value="stats">
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col v-for="(stat, index) in user_stats" :key="index" cols="12" sm="6" md="6" lg="6"
                                xl="3">
                                <v-list-item
                                    :subtitle="user_stats_wordle ? (stat.unit === '%' ? parseFloat(user_stats_wordle[stat.dataName]).toFixed(2) + stat.unit : user_stats_wordle[stat.dataName] + ' ' + stat.unit) : 'N/A'"
                                    :title="stat.title">
                                    <template v-slot:prepend>
                                        <v-avatar color="primary">
                                            <v-icon color="white">{{ stat.icon }}</v-icon>
                                        </v-avatar>
                                    </template>
                                </v-list-item>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-sparkline line-width="0" auto-line-width fill :gradient="gradient"
                    gradient-direction="right"
                    :model-value="user_stats_wordle?.activity || default_sparkline_data" :padding="0"
                    smooth :stroke-linecap="0" type="trend">
                </v-sparkline>
            </v-tabs-window-item>
            <v-tabs-window-item value="guesses">
                <v-card-text>
                    <BarGraph :keys="user_guess_distribution_keys" :values="user_guess_distribution_values" />
                </v-card-text>
            </v-tabs-window-item>
            <v-tabs-window-item value="wordles">
                <v-card-text>
                    <DashboardListCard title="Users Wordles" :items="user_wordles" :loading="user_wordles_loading"
                        :headers="wordleListCardHeaders" icon="mdi-account" :page-change="getUserWordles"
                        :page="user_wordles_page" :num-pagination="7" elevation=0>
                        <v-card-text>
                            <v-row>
                                <v-col cols="12">
                                    <v-row>
                                        <v-col cols="12">
                                            <h6 class="text-h6">
                                                View a player's Wordles to see their performance and progress over time.
                                                You can analyze their guessing patterns, the time taken to solve each
                                                Wordle,
                                                and their overall success rate.
                                            </h6>
                                        </v-col>
                                        <v-col cols="12">
                                            <p>
                                                This detailed view helps in understanding a player's strengths and areas
                                                for improvement.
                                                It also provides insights into their strategic approach to solving
                                                Wordles, making it a valuable tool for both players and analysts.
                                            </p>
                                        </v-col>
                                    </v-row>
                                </v-col>
                            </v-row>
                        </v-card-text>
                    </DashboardListCard>
                </v-card-text>
            </v-tabs-window-item>
        </v-tabs-window>
    </v-card>
</template>

<script>
import { defineComponent, ref, watch, onMounted } from 'vue';
import DashboardListCard from './DashboardListCard.vue';
import { userWordleStats, userWordles } from '@/api/wordle'
import BarGraph from './graphs/BarGraph.vue';
import { useTheme } from 'vuetify';

export default defineComponent({
    name: 'UserViewComponent',
    components: {
        DashboardListCard,
        BarGraph,
    },
    props: {
        slug: {
            type: [String],
            required: true,
        },
    },
    data() {
        return {
            tabs: [
                { title: 'Stats', value: 'stats', icon: 'mdi-chart-bar' },
                { title: 'Guesses', value: 'guesses', icon: 'mdi-lightbulb-outline' },
                { title: 'Wordles', value: 'wordles', icon: 'mdi-format-list-numbered' },
            ],
            user_stats: [
                {
                    icon: 'mdi-chart-line',
                    title: 'Average Guesses',
                    dataName: 'avg_guesses',
                    unit: '',
                },
                {
                    icon: 'mdi-timer',
                    title: 'Average Time',
                    dataName: 'avg_time',
                    unit: 'seconds',
                },
                {
                    icon: 'mdi-check-circle',
                    title: 'Solved Percentage',
                    dataName: 'solved_percentage',
                    unit: '%',
                },
                {
                    icon: 'mdi-format-list-numbered',
                    title: 'Total Wordles',
                    dataName: 'total_wordles',
                    unit: '',
                },
            ],
            wordleListCardHeaders: [
                { title: 'Word', key: 'word' },
                { title: 'Date', key: 'start_time' },
                { title: 'Guesses', key: 'guesses' },
                { title: 'Time', key: 'time' },
            ],
            default_sparkline_data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        };
    },
    setup(props) {
        const defaultPage = {
            count: 10,
            current_page: 1,
            has_next: false,
            has_prev: false,
            page_size: 10,
            total_pages: 1,
        };

        const defaultUser = {
            full_name: '',
            email: '',
            slug: '',
        }

        const activeTab = ref("stats");
        const loading = ref(true);
        const user = ref(defaultUser);
        const user_stats_wordle = ref(null);
        
        const user_wordles = ref([]);
        const user_wordles_loading = ref(false);
        const user_wordles_page = ref(defaultPage);
        const user_guess_distribution_keys = ref([]);
        const user_guess_distribution_values = ref([]);

        const theme = useTheme();
        const gradient = ref([theme.current.value.colors.primary,]);

        const getUserAndStats = async () => {
            loading.value = true;
            try {
                const response = await userWordleStats(props.slug);
                user.value = response.data.user;
                user_stats_wordle.value = response.data.stats;
                const guess_distrubution = response.data.stats.guess_distribution;
                user_guess_distribution_keys.value = Object.keys(guess_distrubution);
                user_guess_distribution_values.value = Object.values(guess_distrubution);
            } catch (error) {
            } finally {
                loading.value = false;
            }
        };

        const getUserWordles = async (page) => {
            user_wordles_loading.value = true;
            try {
                const response = await userWordles(props.slug, page);
                user_wordles.value = response.data.results;
                user_wordles_page.value = response.data.page;
            } catch (error) {
            } finally {
                user_wordles_loading.value = false;
            }
        };


        function getProfilePictureUrl(picture_url) {
            return `/static/profile_pictures/${picture_url}`;
        }

        onMounted(async () => {
            getUserAndStats();
            getUserWordles(1);
        });

        watch(() => props.slug, (newSlug) => {
            getUserAndStats();
            getUserWordles(1);
        });

        return {
            activeTab,
            loading,
            user,
            user_stats_wordle,
            user_wordles,
            user_wordles_loading,
            user_wordles_page,
            getUserWordles,
            user_guess_distribution_keys,
            user_guess_distribution_values,
            getProfilePictureUrl,
            gradient,
        };
    },
});
</script>

<style scoped></style>
