<template>
    <v-card>
        <div style="position: absolute; top: 10px; right: 10px;">
            <v-btn icon @click.stop="dialog = true" elevation="0">
                <v-icon class="icon-style">mdi-information-outline</v-icon>
            </v-btn>
        </div>

        <!-- Loading Indicator -->
        <v-overlay :model-value="loading" class="align-center justify-center" contained>
            <v-progress-circular indeterminate></v-progress-circular>
        </v-overlay>

        <!-- Info Dialog -->
        <v-dialog v-model="dialog" max-width="600px">
            <v-card class="pa-4">
                <v-card-title>
                    <span class="text-h5 font-weight-bold">How To Play</span>
                </v-card-title>
                <v-card-text>
                    <p></p>
                    <ul>
                        <li>Guess the Wordle in 6 tries.</li>
                        <li>Guess the 5-letter word by typing in the input field below the tiles.</li>
                        <li>Each guess must be a valid 5-letter word.</li>
                        <li>The color of the tiles will change to show how close your guess was to the word.</li>
                    </ul>
                    <br />
                    <v-divider />
                    <br />
                    <p class="font-weight-bold">Examples</p>
                    <div class="example-container">
                        <p>
                            <span class="example-tile example-tile-correct">W</span>
                            <span class="example-tile">O</span>
                            <span class="example-tile">R</span>
                            <span class="example-tile">D</span>
                            <span class="example-tile">Y</span>
                        </p>
                        <p class="ml-4">W is in the word and in the correct spot.</p>
                    </div>
                    <div class="example-container">
                        <p>
                            <span class="example-tile">L</span>
                            <span class="example-tile example-tile-wrong-location">I</span>
                            <span class="example-tile">G</span>
                            <span class="example-tile">H</span>
                            <span class="example-tile">T</span>
                        </p>
                        <p class="ml-4">I is in the word but in the wrong spot.</p>
                    </div>
                    <div class="example-container">
                        <p>
                            <span class="example-tile">R</span>
                            <span class="example-tile">O</span>
                            <span class="example-tile">G</span>
                            <span class="example-tile example-tile-wrong">U</span>
                            <span class="example-tile">E</span>
                        </p>
                        <p class="ml-4">U is not in the word in any spot.</p>
                    </div>
                </v-card-text>
                <v-card-actions>
                    <v-btn color="primary" text @click="dialog = false">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <WordleDisplay ref="wordleDisplayRef" :wordLength="wordLength" :numGuesses="numGuesses"
            :throwConfetti="throwConfetti" :flipAnimationDelay="flipAnimationDelay" :preventInput="preventInput"
            :currentTiles="currentTiles" :correctTiles="correctTiles" :onGuessSubmit="onGuessSubmit" />
    </v-card>
</template>

<script>
import WordleDisplay from './WordleDisplay.vue';

export default {
    components: {
        WordleDisplay
    },
    props: {
        wordLength: {
            type: Number,
            required: false,
            default: 5,
        },
        numGuesses: {
            type: Number,
            required: false,
            default: 6,
        },
        throwConfetti: {
            type: Boolean,
            required: false,
            default: false,
        },
        flipAnimationDelay: {
            type: Number,
            required: false,
            default: 150,
        },
        preventInput: {
            type: Boolean,
            required: true,
            default: false,
        },
        currentTiles: {
            type: String,
            required: true
        },
        correctTiles: {
            type: String,
            required: true,
        },
        onGuessSubmit: {
            type: Function,
            required: false,
        },
        loading: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    data() {
        return {
            dialog: false
        };
    },
    setup() {
        const wordleDisplayRef = ref(null);

        const shakeGuess = () => {
            wordleDisplayRef.value?.shakeGuess();
        };

        const showAlert = (message) => {
            wordleDisplayRef.value?.showAlert(message);
        };

        const simulateKey = (key) => {
            if (wordleDisplayRef.value && typeof wordleDisplayRef.value.simulateKey === 'function') {
                wordleDisplayRef.value.simulateKey(key);
            } else {
                console.error('simulateKey is not a function');
            }
        };

        const animateNextTiles = () => {
            if (wordleDisplayRef.value && typeof wordleDisplayRef.value.animateNextTiles === 'function') {
                wordleDisplayRef.value.animateNextTiles();
            } else {
                console.error('animateNextTiles is not a function');
            }
        };

        return {
            wordleDisplayRef,
            shakeGuess,
            showAlert,
            simulateKey,
            animateNextTiles,
        };
    }
};
</script>

<style scoped>
    .example-tile {
        display: inline-block;
        width: 32px;
        height: 32px;
        line-height: 32px;
        text-align: center;
        font-weight: bold;
        color: white;
        margin-right: 4px;
        border: 1px solid #333;
    }

    .example-tile-correct {
        background-color: rgb(43, 114, 186);
    }

    .example-tile-wrong-location {
        background-color: rgb(207, 178, 60);
    }

    .example-tile-wrong {
        background-color: rgb(59, 59, 59);
    }
</style>