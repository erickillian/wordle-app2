<template>
    <v-card max-width="400">
        <v-card-title v-if="wordle?.word">
            {{ wordle?.word ? wordle.word.charAt(0).toUpperCase() + wordle.word.slice(1) : '' }}
        </v-card-title>
        <v-card-subtitle style="margin-bottom: 10px;">
            <p style="white-space: pre-wrap;">
            {{ wordle?.definition ? wordle.definition : `No definition found for ${wordle?.word}` }}
            </p>
        </v-card-subtitle>
    </v-card>
</template>

<script>
export default {
    name: 'WordDefinitionCard',
    props: {
        wordle: {
            type: Object,
            default: () => ({
                slug: "",
                start_time: "",
                solved: false,
                guess_history: "",
                guesses: 0,
                correct: "",
                time: "",
                word: "?????",
            })
        },
    },
};
</script>

<style scoped>

</style>
