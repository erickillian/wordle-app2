import api from './api';

export const guess = async (guess: string) => {
    return api.post('/api/v1/wordle/guess', { guess });
};

export const status = async () => {
    return api.get('/api/v1/wordle/status', {});
};

export const today = async (page: number) => {
    return api.get('/api/v1/wordle/today', { params: { page } });
};

export const shame = async (page: number) => {
    return api.get('/api/v1/wordle/shame', {params: { page }});
};

export const guessesLeaders = async () => {
    return api.get('/api/v1/wordle/leaders/guesses', {});
};

export const timeLeaders = async () => {
    return api.get('/api/v1/wordle/leaders/time', {});
};

export const medalLeaders = async () => {
    return api.get('/api/v1/wordle/leaders/medals', {});
};

export const stats = async () => {
    return api.get('/api/v1/wordle/stats', {});
};

export const wordles = async () => {
    return api.get('/api/v1/wordle/wordles', {});
};

export const wordle = async (slug: string) => {
    return api.get(`/api/v1/wordle/wordle/${slug}`, {});
};

export const userWordles = async (slug: string, page: number) => {
    return api.get(`/api/v1/wordle/user/${slug}/wordles`, {params: { page }});
};

export const userWordleStats = async (slug: string) => {
    return api.get(`/api/v1/wordle/user/${slug}/stats`, {});
};