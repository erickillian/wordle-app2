<template>
    <v-container>
        <v-row class="justify-center">
            <v-col class="" cols="auto">
                <WordleCard ref="wordleDisp" :current-tiles="wordleLetters" :correct-tiles="wordleCorrect"
                    :on-guess-submit="handleGuess" :preventInput="true" />
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import WordleCard from "@/components/wordle/WordleCard.vue";

export default {
    name: "WordlePage",
    components: {
        WordleCard,
    },
    setup() {
        const wordleLetters = ref("");
        const wordleCorrect = ref("");
        const wordleDisp = ref(null); // Define the wordleDisp variable

        const guesses = [
            // Guesses for 'apple'
            "blimpclouddrinkeaglefrostapple",

            // Guesses for 'beach'
            "craneflameglovemangopianobeach",

            // Guesses for 'candy'
            "danceflintgraspplumesweepcandy",

            // Guesses for 'daisy'
            "blinkfrostglareknocksweepdaisy",

            // Guesses for 'emily'
            "flamegrapehorsepianosillyemily",

            // Guesses for 'fairy'
            "blinkclimbgrassshinewheatfairy",

            // Guesses for 'grape'
            "cabindrainmirthplumeswirlgrape",

            // Guesses for 'hazel'
            "blazecrustflintgrovewhalehazel",

            // Guesses for 'jolly'
            "bravecrispfabletrendvividjolly",

            // Guesses for 'kitty'
            "candyflintgrasssweepvividkitty",
        ];
        const correct = [
            "010010100000000010220000022222",   // Guesses for 'apple'
            "102010020100001010000020022222",   // Guesses for 'beach'
            "122100001000100000000000022222",   // Guesses for 'candy'
            "002000002000100000001000022222",   // Guesses for 'daisy'
            "010110000100001010000102222222",   // Guesses for 'emily'
            "002000020001100002000001022222",   // Guesses for 'fairy'
            "010000220000100100020001022222",   // Guesses for 'grape'
            "011110000001000000010111122222",   // Guesses for 'hazel'
            "000000000000020000000000022222",   // Guesses for 'jolly'
            "000020010100000000000200022222",   // Guesses for 'kitty'
        ];

        const currentIndex = ref(0);
        let interval = null;

        const handleGuess = (guess) => {};

        const simulateGame = () => {
            let count = 0;
            interval = setInterval(() => {
                if (count < 12) {
                    if (count % 2 === 0) {
                        // Simulate someone typing the letters
                        const revealedLength = 5 * (Math.floor(count / 2) + 1);
                        const guess = guesses[currentIndex.value].slice(revealedLength-5, revealedLength);
                        for (let i = 0; i < guess.length; i++) {
                            setTimeout(() => {
                                wordleDisp.value.simulateKey(guess[i]);
                            }, i * 300);
                        }
                    } else {
                        // Reveal the next set of letters
                        wordleDisp.value.animateNextTiles();
                        const revealedLength = 5 * (Math.floor(count / 2) + 1);
                        wordleLetters.value = guesses[currentIndex.value].slice(0, revealedLength);
                        wordleCorrect.value = correct[currentIndex.value].slice(0, revealedLength);
                    }
                } else if (count === 12) {
                    // Wait for 2 seconds
                    setTimeout(() => {
                        // Reset for the next round
                        wordleLetters.value = '';
                        wordleCorrect.value = '';
                        count = -1;
                        currentIndex.value = (currentIndex.value + 1) % guesses.length;
                    }, 2000);
                }
                count++;
            }, 2000);
        };

        onMounted(() => {
            simulateGame();
        });

        onUnmounted(() => {
            if (interval) {
                clearInterval(interval);
            }
        });

        return {
            wordleLetters,
            wordleCorrect,
            handleGuess,
            wordleDisp,
        };
    },
};
</script>

<style scoped></style>
