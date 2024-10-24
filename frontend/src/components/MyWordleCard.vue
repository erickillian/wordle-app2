<template>
    <v-card>
        <v-card-title class="d-flex flex-column justify-center align-center stats-container">
            <template v-if="loading">
                <v-progress-circular indeterminate color="primary" class="my-5" />
            </template>
            <template v-else-if="playedToday">
                <v-col class="text-center">
                    <v-icon v-if="dailyRank === 1" class="gold-medal">mdi-crown</v-icon>
                    <v-icon v-else-if="dailyRank === 2" class="silver-medal">mdi-trophy</v-icon>
                    <v-icon v-else-if="dailyRank === 3" class="bronze-medal">mdi-trophy-variant</v-icon>
                    <div v-else class="daily-rank-text">
                        Your Daily Rank: {{ formattedDailyRank }}
                    </div>
                    <h1 class="daily-rank mt-2">{{ formattedDailyRank }}</h1>
                </v-col>
            </template>
            <template v-else>
                <div class="no-played-message">You haven't played Wordle today.</div>
            </template>
        </v-card-title>
        <v-card-subtitle v-if="!loading && playedToday" class="text-center">
            <div>Number of Guesses: <strong>{{ guesses }}</strong></div>
            <div>Time: <strong>{{ time }}</strong></div>
        </v-card-subtitle>
        <v-divider></v-divider>
        <v-card-actions class="d-flex justify-center" v-if="!loading">
            <v-btn :href="'/wordle'" color="primary" dark class="play-btn mx-2" large v-ripple block>
            {{ playedToday ? 'See Your Wordle' : 'Play Wordle' }}
            </v-btn>
        </v-card-actions>
        <canvas id="confetti-canvas"></canvas>
    </v-card>
</template>

<script>
import { status } from '@/api/wordle';
import ConfettiGenerator from 'confetti-js';

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

                // Trigger confetti when loaded and played today
                if (this.playedToday) {
                    this.triggerConfetti();
                }
            } catch (error) {
                console.error('Error fetching Wordle status:', error);
            } finally {
                this.loading = false;
            }
        },
        triggerConfetti() {
            const confettiSettings = {
                target: 'confetti-canvas',
                size: 3, // Increase this value for larger confetti pieces (default is 1)
                max: 150, // Number of confetti pieces
                animate: true,
                props: ['circle', 'square', 'triangle'], // Optional: customize shapes
                colors: [[165, 104, 246], [230, 61, 135], [0, 199, 228], [253, 214, 126]], // Custom colors
                clock: 25, // Speed of confetti fall
                rotate: true, // Rotate confetti pieces
                start_from_edge: false, // Start confetti from edges
                respawn: true, // Do not respawn confetti
            };
            const confetti = new ConfettiGenerator(confettiSettings);
            confetti.render();
            setTimeout(() => {
            const canvas = document.getElementById('confetti-canvas');
            if (canvas) {
                canvas.style.transition = 'opacity 2s ease';
                canvas.style.opacity = '0';
            }
            }, 5000); // Start fading after 5 seconds
        },
    },
    mounted() {
        this.fetchWordleStatus();
    },
};
</script>

<style scoped>
.stats-container {
    text-align: center;
}

.daily-rank {
    font-size: 3.5em;
    font-weight: bold;
}

.no-played-message {
    font-size: 1.5em;
    color: #b0bec5;
    text-align: center;
    margin: 20px;
}

.play-btn {
    font-size: 1.2em;
    font-weight: bold;
}

.gold-medal {
    font-size: 3.5em;
    color: #ffd700;
}

.silver-medal {
    font-size: 3.5em;
    color: #c0c0c0;
}

.bronze-medal {
    font-size: 3.5em;
    color: #cd7f32;
}

/* Confetti canvas overlay */
#confetti-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 999;
    /* High z-index to appear above other elements */
    pointer-events: none;
    /* Prevent interaction with the canvas */
}
</style>
