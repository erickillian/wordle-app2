<template>
    <v-card style="height: 100%">
        <v-card-title class="py-2">
            <v-row justify="center" class="my-0">
                <v-col cols="auto" class="text-center">
                    <h1 style="font-size: 2rem; text-align: center;">{{ word }}</h1>
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
                            <v-col v-for="(stat, index) in user_stats" :key="index" cols="12" sm="6" md="6" lg="6" xl="3">
                                <v-list-item
                                    :subtitle="word_stats ? (stat.unit === '%' ? parseFloat(word_stats[stat.dataName]).toFixed(2) + stat.unit : word_stats[stat.dataName] + ' ' + stat.unit) : 'N/A'"
                                    :title="stat.title">
                                    <template v-slot:prepend>
                                        <v-avatar color="primary">
                                            <v-icon color="white">{{ stat.icon }}</v-icon>
                                        </v-avatar>
                                    </template>
                                </v-list-item>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="12">
                                <WordDefintionCard word="Definition:" :definition="word_definition" :elevation="0"  />
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
            </v-tabs-window-item>
            <v-tabs-window-item value="guesses">
                <v-card-text>
                    <BarGraph :keys="word_guess_keys" :values="word_guess_values" />
                </v-card-text>
            </v-tabs-window-item>
            <v-tabs-window-item value="wordles">
                <v-card-text>
                    <DashboardListCard title="Word Wordles" :items="word_wordles" :loading="word_wordles_loading"
                        :headers="wordleListCardHeaders" icon="mdi-account" :page-change="getWordWordles"
                        :page="word_wordles_page" :num-pagination="7" elevation=0>
                        <v-card-text>
                            <v-row>
                                <v-col cols="12">
                                    <v-row>
                                        <v-col cols="12">
                                            <h6 class="text-h6">
                                                View the users who have guessed this word to see their performance.
                                                You can analyze their guessing patterns, the time taken to solve the
                                                word,
                                                and their overall success rate.
                                            </h6>
                                        </v-col>
                                        <v-col cols="12">
                                            <p>
                                                This detailed view helps in understanding how different users approach
                                                the word.
                                                It provides insights into their guessing strategies and areas for
                                                improvement,
                                                making it a valuable tool for both players and analysts.
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
import { word as wordInfo, wordWordles } from '@/api/wordle'
import BarGraph from './graphs/BarGraph.vue';
import { useTheme } from 'vuetify';
import { guess } from '@/api/auth';
import WordDefintionCard from '@/components/wordle/WordDefinitionCard.vue';

export default defineComponent({
    name: 'WordViewViewComponent',
    components: {
        DashboardListCard,
        BarGraph,
        WordDefintionCard,
    },
    props: {
        word: {
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
                { title: 'Rank', key: 'rank' },
                { title: 'User', key: 'user' },
                { title: 'Date', key: 'start_time' },
                { title: 'Guesses', key: 'guesses' },
                { title: 'Time', key: 'time' },
            ],
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

        const defaultWord = {
            word: '',
            definition: '',
        }

        const activeTab = ref("stats");
        const loading = ref(true);
        const word_stats = ref(null);

        const word_wordles = ref([]);
        const word_wordles_loading = ref(false);
        const word_wordles_page = ref(defaultPage);
        const word_guess_keys = ref([]);
        const word_guess_values = ref([]);
        const word_definition = ref('');

        const getWordStats = async () => {
            loading.value = true;
            try {
                const response = await wordInfo(props.word);
                word_stats.value = response.data.stats;
                const guess_distrubution = response.data.guess_distribution;
                word_guess_keys.value = Object.keys(guess_distrubution);
                word_guess_values.value = Object.values(guess_distrubution);
                word_definition.value = response.data.definition;
            } catch (error) {
            } finally {
                loading.value = false;
            }
        };

        const getWordWordles = async (page) => {
            word_wordles_loading.value = true;
            try {
                const response = await wordWordles(props.word, page);
                word_wordles.value = response.data.results;
                word_wordles_page.value = response.data.page;
            } catch (error) {
            } finally {
                word_wordles_loading.value = false;
            }
        };

        onMounted(async () => {
            getWordStats();
            getWordWordles(1);
        });

        watch(() => props.word, (newWord) => {
            getWordStats();
            getWordWordles(1);
        });

        return {
            activeTab,
            loading,
            word_stats,
            word_wordles,
            word_wordles_loading,
            word_wordles_page,
            word_definition,
            getWordWordles,
            word_guess_keys,
            word_guess_values,
        };
    },
});
</script>

<style scoped></style>
