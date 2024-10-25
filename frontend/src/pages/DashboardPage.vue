<template>
    <v-container fluid>
        <v-row>
            <v-col cols="12" xl="6" lg="5" md="12">
                <v-row>
                    <v-col cols="12">
                        <MyWordleCard />
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="12">
                        <DashboardListCard title="Today's Wordles" :items="todays_wordles" :loading="todays_wordles_loading"
                            :headers="todaysWordlesHeaders" icon="mdi-calendar-today" :page-change="getTodaysWordles"
                            :page="todays_wordles_page" rank-items>
                            <v-card-text>
                                <v-row>
                                    <v-col cols="12">
                                        <h6 class="text-h6">
                                            Today's Wordles showcase the top players of the day. The first three
                                            places
                                            are awarded medals:
                                        </h6>
                                    </v-col>
                                    <v-col cols="12">
                                        <v-list dense>
                                            <v-list-item>
                                                <v-list-item-title><strong>1st Place:</strong> Gold Medal
                                                    🥇</v-list-item-title>
                                            </v-list-item>
                                            <v-list-item>
                                                <v-list-item-title><strong>2nd Place:</strong> Silver Medal
                                                    🥈</v-list-item-title>
                                            </v-list-item>
                                            <v-list-item>
                                                <v-list-item-title><strong>3rd Place:</strong> Bronze Medal
                                                    🥉</v-list-item-title>
                                            </v-list-item>
                                        </v-list>
                                    </v-col>
                                    <v-col cols="12">
                                        <p>
                                            Players are ranked primarily by the number of guesses they took to solve
                                            the
                                            Wordle. In case of a tie, the time taken to solve the Wordle is used as
                                            the
                                            tiebreaker. This ensures a fair and competitive environment where both
                                            accuracy and speed are rewarded.
                                        </p>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </DashboardListCard>
                    </v-col>
                </v-row>
            </v-col>

            <v-col cols="12" xl="6" lg="7" md="12">
                <v-row rows="12">
                    <v-col cols="12" xl="6" lg="6" md="12" sm="12">
                        <DashboardListCard title="Wordle Leaders - Guesses" :items="wordle_leaders_guesses"
                            :loading="wordle_leaders_guesses_loading" :headers="wordleGuessesLeadersHeaders"
                            icon="mdi-trophy" rank-items>
                            <v-card-text>
                                <v-row>
                                    <v-col cols="12">
                                        <h6 class="text-h6">
                                            Wordle Leaders - Guesses showcases the top players based on their
                                            average
                                            number of guesses.
                                        </h6>
                                    </v-col>
                                    <v-col cols="12" class="text-center">
                                        <v-img src="@/assets/guesses_leaders.jpg" alt="Guesses Leaders"
                                            max-width="400"></v-img>
                                    </v-col>
                                    <v-col cols="12">
                                        <p>
                                            The average number of guesses is calculated by taking the total number
                                            of
                                            guesses a player has made across all Wordles and dividing it by the
                                            number
                                            of Wordles they have solved. This metric highlights players who
                                            consistently
                                            solve Wordles with fewer guesses, demonstrating their skill and
                                            strategy.
                                        </p>
                                    </v-col>
                                    <v-col cols="12">
                                        <p>
                                            Note: To appear on this leaderboard, you must have completed at least 10
                                            Wordles. This ensures that the rankings are based on a sufficient number
                                            of
                                            games to accurately reflect a player's skill and consistency.
                                        </p>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </DashboardListCard>
                    </v-col>
                    <v-col cols="12" xl="6" lg="6" md="12" sm="12">
                        <DashboardListCard title="Wordle Leaders - Time" :items="wordle_leaders_time"
                            :loading="wordle_leaders_time_loading" :headers="wordleTimeLeadersHeaders" icon="mdi-trophy"
                            rank-items>
                            <v-card-text>
                                <v-row>
                                    <v-col cols="12">
                                        <h6 class="text-h6">
                                            Wordle Leaders - Time showcases the top players based on their average
                                            time
                                            to solve Wordles.
                                        </h6>
                                    </v-col>
                                    <v-col cols="12" class="text-center">
                                        <v-img src="@/assets/time_leaders.jpg" alt="Time Leaders"
                                            max-width="400"></v-img>
                                    </v-col>
                                    <v-col cols="12">
                                        <p>
                                            The average time is calculated by taking the total time a player has
                                            spent
                                            solving Wordles and dividing it by the number of Wordles they have
                                            solved.
                                            This metric highlights players who consistently solve Wordles quickly,
                                            demonstrating their speed and efficiency.
                                        </p>
                                    </v-col>
                                    <v-col cols="12">
                                        <p>
                                            Note: To appear on this leaderboard, you must have completed at least 10
                                            Wordles. This ensures that the rankings are based on a sufficient number
                                            of
                                            games to accurately reflect a player's skill and consistency.
                                        </p>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </DashboardListCard>
                    </v-col>
                    <v-col cols="12" xl="12" lg="12" md="12" sm="12">
                        <DashboardListCard title="Wordle Leaders - Medals" :items="wordle_leaders_medals"
                            :loading="wordle_leaders_medals_loading" :headers="wordleMedalLeadersHeaders"
                            icon="mdi-trophy" rank-items>
                            <v-card-text>
                                <v-row>
                                    <v-col cols="12">
                                        <h6 class="text-h6">
                                            Wordle Leaders - Medals showcases the top players based on the number of
                                            medals they have earned.
                                        </h6>
                                    </v-col>
                                    <v-col cols="12" class="text-center">
                                        <v-img src="@/assets/medals_leaders.jpg" alt="Medals Leaders"
                                            max-width="400"></v-img>
                                    </v-col>
                                    <v-col cols="12">
                                        <p>
                                            This leaderboard calculates the number of gold, silver, and bronze
                                            medals a
                                            user has. Medals are converted into points: gold = 3, silver = 2, and
                                            bronze
                                            = 1. Users are primarily sorted by the number of gold medals. In case of
                                            a
                                            tie, the total points are used to determine the ranking.
                                        </p>
                                        <p>
                                            A gold medal is awarded to the player who solved a Wordle with the
                                            fewest
                                            guesses for that day. Silver is for the second fewest, and bronze for
                                            the
                                            third. In case of a tie in the number of guesses, the time taken to
                                            solve
                                            the Wordle is used as a tiebreaker.
                                        </p>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </DashboardListCard>
                    </v-col>
                    <v-col cols="12" xl="12" lg="12" md="12" sm="12">
                        <DashboardListCard title="Wall of Shame" :items="wordle_shame" :loading="wordle_shame_loading"
                            :headers="wordleWallOfShameHeaders" :page-change="getWallOfShame" :page="wordle_shame_page"
                            icon="mdi-emoticon-sad-outline">
                            <v-card-text>
                                <v-row>
                                    <v-col cols="12">
                                        <h6 class="text-h6">
                                            Wall of Shame highlights the players who failed to complete their
                                            Wordles.
                                        </h6>
                                    </v-col>
                                    <v-col cols="12" class="text-center">
                                        <v-img src="@/assets/shameful_image.jpg" alt="Shameful Image"
                                            max-width="400"></v-img>
                                    </v-col>
                                    <v-col cols="12">
                                        <p>
                                            This section serves as a public reminder of the players who couldn't
                                            complete their Wordles. It aims to encourage players to improve their
                                            strategies and strive for better performance in future games.
                                        </p>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </DashboardListCard>
                    </v-col>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import BigNumberCard from '@/components/BigNumberCard.vue';
import DashboardListCard from '@/components/DashboardListCard.vue';
import MyWordleCard from '@/components/MyWordleCard.vue';
import { shame, guessesLeaders, timeLeaders, medalLeaders, today } from "@/api/wordle";
import { Page } from "@/types/index";

export default defineComponent({
    name: 'DashboardPage',
    components: {
        BigNumberCard,
        DashboardListCard,
        MyWordleCard,
    },
    data() {
        return {
            todaysWordlesHeaders: [
                {
                    key: 'user',
                    title: 'User'
                },
                {
                    key: 'word',
                    title: 'Word'
                },
                {
                    key: 'guesses',
                    title: 'Guesses'
                },
                {
                    key: 'time',
                    title: 'Time',
                },
            ],
            wordleWallOfShameHeaders: [
                {
                    key: 'user',
                    title: 'User'
                },
                {
                    key: 'word',
                    title: 'Word'
                },
                {
                    key: 'start_time',
                    title: 'Date'
                },
                {
                    key: 'guesses',
                    title: 'Guesses'
                },
                {
                    key: 'time',
                    title: 'Time'
                }
            ],
            wordleGuessesLeadersHeaders: [
                {
                    key: 'user',
                    title: 'User'
                },
                {
                    key: 'avg_guesses',
                    title: 'Average Guesses'
                },
            ],
            wordleTimeLeadersHeaders: [
                {
                    key: 'user',
                    title: 'User'
                },
                {
                    key: 'avg_time',
                    title: 'Average Time'
                },
            ],
            wordleMedalLeadersHeaders: [
                {
                    key: 'user',
                    title: 'User'
                },
                {
                    key: 'gold_medals',
                    title: 'Gold Medals'
                },
                {
                    key: 'silver_medals',
                    title: 'Silver Medals'
                },
                {
                    key: 'bronze_medals',
                    title: 'Bronze Medals'
                },
                {
                    key: 'total_points',
                    title: 'Total Points'
                }
            ]
        }
    },
    setup() {
        const defaultPage: Page = {
            count: 10,
            current_page: 1,
            has_next: false,
            has_prev: false,
            page_size: 10,
            total_pages: 1,
        }
        
        const todays_wordles = ref([])
        const todays_wordles_loading = ref(false)
        const todays_wordles_page = ref(defaultPage)
        const wordle_shame = ref([])
        const wordle_shame_loading = ref(false)
        const wordle_shame_page = ref(defaultPage)
        const wordle_leaders_guesses = ref([])
        const wordle_leaders_guesses_loading = ref(false)
        const wordle_leaders_time = ref([])
        const wordle_leaders_time_loading = ref(false)
        const wordle_leaders_medals = ref([])
        const wordle_leaders_medals_loading = ref(false)

        const getTodaysWordles = async (page: number) => {
            todays_wordles_loading.value = true;
            try {
                const response = await today(page);
                // Handle the results here, e.g., update the state
                todays_wordles.value = response.data.results;
                todays_wordles_page.value = response.data.page;
            } catch (error) {
                todays_wordles_page.value = defaultPage;
            } finally {
                todays_wordles_loading.value = false;
            }
        };

        const getWallOfShame = async (page: number) => {
            wordle_shame_loading.value = true;
            try {
                const response = await shame(page);
                // Handle the results here, e.g., update the state
                wordle_shame.value = response.data.results;
                wordle_shame_page.value = response.data.page;
            } catch (error) {
            } finally {
                wordle_shame_loading.value = false;
            }
        };

        const getWordleLeadersGuesses = async () => {
            wordle_leaders_guesses_loading.value = true;
            wordle_leaders_guesses.value = [];
            try {
                const response = await guessesLeaders();
                // Handle the results here, e.g., update the state
                wordle_leaders_guesses.value = response.data;
            } catch (error) {
            } finally {
                wordle_leaders_guesses_loading.value = false;
            }
        };

        const getWordleLeadersTime = async () => {
            wordle_leaders_time_loading.value = true;
            wordle_leaders_time.value = [];
            try {
            const response = await timeLeaders();
            // Handle the results here, e.g., update the state
            wordle_leaders_time.value = response.data;
            } catch (error) {
            } finally {
            wordle_leaders_time_loading.value = false;
            }
        };

        const getWordleLeadersMedals = async () => {
            wordle_leaders_medals_loading.value = true;
            wordle_leaders_medals.value = [];
            try {
            const response = await medalLeaders();
            // Handle the results here, e.g., update the state
            wordle_leaders_medals.value = response.data;
            } catch (error) {
            } finally {
            wordle_leaders_medals_loading.value = false;
            }
        };

        onMounted(() => {
            getTodaysWordles(1);
            getWallOfShame(1);
            getWordleLeadersGuesses();
            getWordleLeadersTime();
            getWordleLeadersMedals();
        });

        return {
            getTodaysWordles,
            getWallOfShame,
            todays_wordles,
            todays_wordles_loading,
            todays_wordles_page,
            wordle_shame,
            wordle_shame_loading,
            wordle_shame_page,
            wordle_leaders_guesses,
            wordle_leaders_guesses_loading,
            wordle_leaders_time,
            wordle_leaders_time_loading,
            wordle_leaders_medals,
            wordle_leaders_medals_loading,
        };
    }
});
</script>

<style scoped>
/* You can add custom styles here if necessary */
</style>
