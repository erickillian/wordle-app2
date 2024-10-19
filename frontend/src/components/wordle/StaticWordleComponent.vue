<template>
    <v-row class="justify-center">
        <v-col class="" cols="auto">
            <WordleDisplay ref="wordleDisp" prevent-input :current-tiles="wordle.guess_history"
                :correct-tiles="wordle.correct" />
        </v-col>
        <v-col cols="auto">
            <v-row>
                <v-col>
                    <TimeClockComponent :time="wordle.time" :start-time="wordle.start_time"
                        :elapsed-time="wordle.time" />

                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <WordDefinitionCard :wordle="wordle" />
                </v-col>
            </v-row>
            <v-row v-if="wordle?.word">
                <v-col>
                    <ExtraWordleRankingsCard :wordle="wordle" />
                </v-col>
            </v-row>
        </v-col>
    </v-row>
</template>

<script>
import { ref, onMounted } from 'vue';
import WordleDisplay from "@/components/wordle/WordleDisplay.vue";
import TimeClockComponent from '@/components/wordle/TimeClockComponent.vue';
import WordDefinitionCard from '@/components/wordle/WordDefinitionCard.vue';
import ExtraWordleRankingsCard from '@/components/wordle/ExtraWordleRankingsCard.vue';
import { wordle as fetchWordle } from '@/api/wordle';

export default {
    name: "StaticWordleComponent",
    components: {
        WordleDisplay,
        TimeClockComponent,
        ExtraWordleRankingsCard,
    },
    props: {
        slug: {
            type: String,
            required: true,
        },
    },
    setup(props) {
        const wordle = ref({
            slug: "",
            start_time: "",
            solved: false,
            guess_history: "",
            guesses: 0,
            correct: "",
            time: "",
        });
        const wordleDisp = ref(null);

        const getWordle = async () => {
            try {
                const response = await fetchWordle(props.slug);
                Object.assign(wordle.value, { ...response.data });
            } catch (error) {
                // Handle error
            }
        };

        onMounted(() => {
            getWordle();
        });

        return {
            wordle,
            wordleDisp,
        };
    },
};
</script>

<style scoped></style>
