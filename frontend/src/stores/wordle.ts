// stores/wordleStore.ts

import { defineStore } from 'pinia';
import * as wordleApi from '../api/wordle';


// Define the Pinia store
export const useWordleStore = defineStore('wordle', {
    state: () => ({
        wordle: {},
        error: null as string | null,
        wordle_loading: false,
        guess_loading: false,
    }),
    actions: {
        async getWordleStatus() {
            this.wordle_loading = true;
            try {
                const response = await wordleApi.status();
                this.wordle = response.data;
                this.error = null;
            } catch (error) {
                console.log(error);
                this.error = (error as Error).message;
            } finally {
                this.wordle_loading = false;
            }
        },
        async makeGuess(guess: string) {
            this.guess_loading = true;
            try {
                const response = await wordleApi.guess(guess);
                this.wordle = response.data;
            } catch (error) {
                this.error = (error as Error).message;
            } finally {
                this.guess_loading = false;
            }
        },
        async getWordle(slug: string) {
            this.wordle_loading = true;
            this.wordle = {};
            try {
                const response = await wordleApi.wordle(slug);
                this.wordle = response.data;
                this.error = null;
            } catch (error) {
                this.error = (error as Error).message;
            } finally {
                this.wordle_loading = false;
            }
        },
    },
});
