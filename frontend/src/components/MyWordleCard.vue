<template>
    <v-card class="mx-auto" style="height: 300px;" @click="navigateToWordle" v-bind:ripple>
        <v-card-title class="d-flex flex-column justify-center align-center stats-container" style="height: 250px;">
            <template v-if="loading">
                <v-progress-circular indeterminate class="my-5" />
            </template>
            <template v-else-if="playedToday">
                <v-icon v-if="dailyRank === 1" class="gold-medal ma-0">mdi-crown</v-icon>
                <v-icon v-else-if="dailyRank === 2" class="silver-medal ma-0">mdi-crown</v-icon>
                <v-icon v-else-if="dailyRank === 3" class="bronze-medal ma-0">mdi-crown</v-icon>
                <v-icon v-else class="daily-rank-icon mb-1">mdi-trophy</v-icon>
                <h1 class="daily-rank">{{ formattedDailyRank }}</h1>
            </template>
            <template v-else>
                <div class="no-played-message">You haven't played Wordle today.</div>
            </template>
            <v-card-subtitle v-if="!loading && playedToday" class="text-center">
                <div>Number of Guesses: <strong>{{ guesses }}</strong></div>
                <div>Time: <strong>{{ time }}</strong></div>
            </v-card-subtitle>
        </v-card-title>

        <v-divider></v-divider>
        <v-card-actions class="d-flex justify-center align-center text-center">
            <v-card-subtitle v-if="!loading">
                {{ playedToday ? 'See Your Wordle' : 'Play Wordle' }}
                <v-icon right>mdi-open-in-new</v-icon>
            </v-card-subtitle>
        </v-card-actions>
        <canvas id="confetti-canvas"></canvas>
    </v-card>
</template>

<script>
import { status } from '@/api/wordle';
import ConfettiGenerator from 'confetti-js';
import { useTheme } from 'vuetify';
import { onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';

export default {
    name: 'MyWordleCard',
    setup() {
        const theme = useTheme();
        const loading = ref(true);
        const playedToday = ref(false);
        const word = ref('');
        const time = ref('');
        const guesses = ref(0);
        const streak = ref(0);
        const definition = ref('');
        const dailyRank = ref(0);
        const wordRank = ref(0);

        const router = useRouter();

        const formattedDailyRank = computed(() => formatRank(dailyRank.value));
        const formattedWordRank = computed(() => formatRank(wordRank.value));

        const formatRank = (rank) => {
            if (!rank) return 'N/A';
            const suffixes = ['th', 'st', 'nd', 'rd'];
            const v = rank % 100;
            return rank + (suffixes[(v - 20) % 10] || suffixes[v] || suffixes[0]);
        };

        const fetchWordleStatus = async () => {
            try {
                const response = await status();
                const data = response.data;
                playedToday.value = !!data.daily_rank;
                word.value = data.word;
                time.value = data.time;
                guesses.value = data.guesses;
                streak.value = data.streak;
                definition.value = data.definition;
                dailyRank.value = data.daily_rank;
                wordRank.value = data.word_rank;

                // Trigger confetti when loaded and played today
                if (playedToday.value) {
                    triggerConfetti();
                }
            } catch (error) {
                console.error('Error fetching Wordle status:', error);
            } finally {
                loading.value = false;
            }
        };

        const triggerConfetti = () => {
            let colors;
            if (dailyRank.value === 1) {
                colors = [[255, 215, 0]]; // Gold
            } else if (dailyRank.value === 2) {
                colors = [[192, 192, 192]]; // Silver
            } else if (dailyRank.value === 3) {
                colors = [[205, 127, 50]]; // Bronze
            } else {
                const isDarkMode = theme.current.value.dark;
                console.log(theme.current.value.dark)
                colors = isDarkMode ? [[255, 255, 255]] : [[0, 0, 0]]; // White for dark mode, Black for light mode
            }

            const confettiSettings = {
                target: 'confetti-canvas',
                size: 2, // Increase this value for larger confetti pieces (default is 1)
                max: 150, // Number of confetti pieces
                animate: true,
                props: ['circle', 'square', 'triangle'], // Optional: customize shapes
                colors: colors, // Custom colors based on rank
                clock: 25, // Speed of confetti fall
                rotate: true, // Rotate confetti pieces
                start_from_edge: false, // Start confetti from edges
                respawn: true, // Do not respawn confetti
            };
            const confetti = new ConfettiGenerator(confettiSettings);
            confetti.render();
            // setTimeout(() => {
            //     const canvas = document.getElementById('confetti-canvas');
            //     if (canvas) {
            //         canvas.style.transition = 'opacity 2s ease';
            //         canvas.style.opacity = '0';
            //     }
            // }, 10000); // Start fading after 5 seconds
        };

        const navigateToWordle = () => {
            router.push('/wordle');
        };

        onMounted(() => {
            fetchWordleStatus();
        });

        return {
            loading,
            playedToday,
            word,
            time,
            guesses,
            streak,
            definition,
            dailyRank,
            wordRank,
            formattedDailyRank,
            formattedWordRank,
            triggerConfetti,
            navigateToWordle,
        };
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
