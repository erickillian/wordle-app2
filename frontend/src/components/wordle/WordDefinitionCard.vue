<template>
    <v-card max-width="400" :elevation="elevation">
        <v-card-title v-if="word">
            {{ word.charAt(0).toUpperCase() + word.slice(1) }}
        </v-card-title>
        <v-card-subtitle style="margin-bottom: 10px;">
            <p style="white-space: pre-wrap;">
            {{ definition ? definition : `No definition found for ${word}` }}
            </p>
        </v-card-subtitle>
    </v-card>
</template>

<script>
export default {
    name: 'WordDefinitionCard',
    props: {
        word: {
            type: String,
            default: ""
        },
        definition: {
            type: String,
            default: ""
        },
        elevation: {
            type: Number,
            default: 2
        }
    },
};
</script>

<style scoped>

</style>
