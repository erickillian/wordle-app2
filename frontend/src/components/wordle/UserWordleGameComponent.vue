<template>
    <v-row class="justify-center">
        <v-col cols="auto">
            <WordleDisplay ref="wordleDisp" :prevent-input="disableInput" :current-tiles="wordle.guess_history"
                :correct-tiles="wordle.correct" :on-guess-submit="handleGuess" :num-guesses="wordle.guesses"
                throw-confetti />
        </v-col>
        <v-col cols="auto">
            <v-row>
                <v-col>
                    <TimeClockComponent :time="wordle.time" :start-time="wordle.start_time"
                        :elapsed-time="wordle.time" />

                </v-col>
            </v-row>
            <v-row v-if="wordle?.word">
                <v-col>
                    <WordDefinitionCard :wordle="wordle" />
                </v-col>
            </v-row>
            <v-row v-if="wordle?.word">
                <v-col>
                    <ExtraWordleRankingsCard :wordle="wordle" />
                </v-col>
            </v-row>
            <v-row v-if="wordle?.word">
                <v-col>
                    <NextWordleCard />
                </v-col>
            </v-row>
        </v-col>
    </v-row>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import WordleDisplay from "@/components/wordle/WordleDisplay.vue";
import TimeClockComponent from '@/components/wordle/TimeClockComponent.vue';
import NextWordleCard from '@/components/wordle/NextWordleCard.vue';
import ExtraWordleRankingsCard from '@/components/wordle/ExtraWordleRankingsCard.vue';
import { guess, status } from '@/api/wordle';

export default {
    name: "UserWordleGameComponent",
    components: {
        WordleDisplay,
        TimeClockComponent,
        NextWordleCard,
        ExtraWordleRankingsCard,
    },
    setup() {
        const wordle = ref({
            slug: "",
            start_time: "",
            solved: false,
            guess_history: "",
            guesses: 0,
            correct: "",
            time: "",
        });
        const disableInput = ref(true);
        const wordleDisp = ref(null); // Ref to the wordleDisp
    
        const handleGuess = async (guess_input) => {
            disableInput.value = true;
            try {
                const response = await guess(guess_input);
                Object.assign(wordle.value, { ...response.data });
                disableInput.value = response.data.solved;

            } catch (error) {
                console.log(error.response.data);
                disableInput.value = false;
                wordleDisp.value.shakeGuess();
                if (error.response.data?.guess)
                    wordleDisp.value.showAlert(error.response.data.guess);
                if (error.response.data?.error)
                    wordleDisp.value.showAlert(error.response.data.error);
            }
        };
    
        onMounted(async () => {
            try {
                const response = await status();
                Object.assign(wordle.value, { ...response.data });
                disableInput.value = response.data.solved;
            } catch (error) {
                
            }
        });
    
        return {
            wordle,
            disableInput,
            handleGuess,
            wordleDisp,
        };
    },
};
</script>


<style scoped>

</style>