<template>
    <v-container fluid>
        <StaticWordleComponent v-if="slug" :slug="slug" />
        <UserWordleGameComponent v-else />
    </v-container>
</template>

<script>
import UserWordleGameComponent from "@/components/wordle/UserWordleGameComponent.vue";
import StaticWordleComponent from "@/components/wordle/StaticWordleComponent.vue";

export default {
    name: "WordlePage",
    components: {
        UserWordleGameComponent,
    },
    props: {
        slug: {
            type: String,
            required: false,
        },
    },
};
</script>