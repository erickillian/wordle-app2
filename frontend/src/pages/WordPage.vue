<template>
    <v-row dense class="mx-0">
        <v-navigation-drawer app :clipped="true" width="500" v-model="showSider" elevation="0">
            <WordsSearchComponent :onWordSelected="onWordSelect" :selectedWord="selectedWord" />
        </v-navigation-drawer>
        <v-col>
            <v-container fluid class="pa-4">
                <template v-if="selectedWord">
                    <WordViewComponent :word="selectedWord" />
                </template>
                <template v-else>
                    <v-alert color="primary" type="info" class="mt-4">
                        Please select a word to view its information.
                    </v-alert>
                </template>
            </v-container>
        </v-col>
        <v-fab class="d-xs-flex d-sm-flex d-lg-none rounded-circle" location="bottom right" size="64" absolute app
            color="primary" @click="toggleSider" rounded="circle">
            <v-icon>mdi-book</v-icon>
        </v-fab>
    </v-row>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue';
import WordsSearchComponent from '@/components/WordsSearchComponent.vue';
import WordViewComponent from '@/components/WordViewComponent.vue';
import { useRouter } from 'vue-router';
import { useDisplay } from 'vuetify';

export default defineComponent({
    name: 'WordDictionaryPage',
    components: {
        WordsSearchComponent,
        WordViewComponent
    },
    props: {
        word: {
            type: String,
            required: false
        }
    },
    setup(props) {
        const router = useRouter();
        const selectedWord = ref<string>('');
        const showSider = ref<boolean>(true);

        watch(() => props.word, (word: string | undefined | null): void => {
            if (word !== undefined && word !== null) {
            selectedWord.value = word;
            } else {
            selectedWord.value = '';
            }
        });

        onMounted((): void => {
            if (props.word !== undefined && props.word !== null) {
            selectedWord.value = props.word;

            const { xs, sm, md } = useDisplay();
            if (xs.value || sm.value || md.value) {
                showSider.value = false;
            }
            }
        });

        const onWordSelect = (word: string | null | undefined): void => {
            if (word !== undefined && word !== null && word !== '') {
            router.push(`/words/${word}`);
            selectedWord.value = word;
            } else {
            router.push('/words');
            selectedWord.value = '';
            }
        };

        const toggleSider = (): void => {
            showSider.value = !showSider.value;
        };

        return {
            selectedWord,
            showSider,
            onWordSelect,
            toggleSider,
        };
    }
});
</script>

<style scoped></style>
