<template>
    <v-card>
        <v-card-subtitle v-if="loading" class="loader-container">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-card-subtitle>
        <v-card-subtitle v-else-if="playedToday" class="stats-container">
            <div class="daily-rank">{{ formattedDailyRank }}</div>
            <div>Number of Guesses: {{ guesses }}</div>
            <div>Word Rank: {{ formattedWordRank }}</div>
        </v-card-subtitle>
        <v-card-subtitle v-else>
            <div>You haven't played Wordle today.</div>
        </v-card-subtitle>
        <v-card-actions>
            <v-btn :href="'/wordle'" color="primary">
                {{ playedToday ? 'See Your Wordle' : 'Play Wordle' }}
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
import { status } from '@/api/wordle';

export default {
    name: 'MyWordleCard',
    data() {
        return {
            loading: true,
            playedToday: false,
            wordle: '',
            time: '',
            guesses: 0,
            streak: 0,
            definition: '',
            dailyRank: 0,
            wordRank: 0,
        };
    },
    computed: {
        formattedDailyRank() {
            return this.formatRank(this.dailyRank);
        },
        formattedWordRank() {
            return this.formatRank(this.wordRank);
        },
    },
    methods: {
        formatRank(rank) {
            if (!rank) return 'N/A';
            const suffixes = ['th', 'st', 'nd', 'rd'];
            const v = rank % 100;
            return rank + (suffixes[(v - 20) % 10] || suffixes[v] || suffixes[0]);
        },
        async fetchWordleStatus() {
            try {
                const response = await status();
                const data = response.data;
                this.playedToday = !!data.daily_rank;
                this.word = data.word;
                this.time = data.time;
                this.guesses = data.guesses;
                this.streak = data.streak;
                this.definition = data.definition;
                this.dailyRank = data.daily_rank;
                this.wordRank = data.word_rank;
            } catch (error) {
                console.error('Error fetching Wordle status:', error);
            } finally {
                this.loading = false;
            }
        },
    },
    mounted() {
        this.fetchWordleStatus();
    },
};
</script>

<style scoped>
.ml-2 {
    margin-left: 8px;
}
.loader-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
}
.stats-container {
    text-align: center;
}
.daily-rank {
    font-size: 4em;
    font-weight: bold;
    margin-bottom: 16px;
}
</style>