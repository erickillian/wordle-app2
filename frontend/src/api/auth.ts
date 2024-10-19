import api from './api';

export const guess = async (guess: string) => {
    return api.post('/api/v1/wordle/guess', { guess });
};

export const login = async (email: string, password: string) => {
    return api.post('/api/v1/user/login', { email, password });
};

export const logout = async (refresh: string) => {
    return api.post('/api/v1/user/logout', { refresh });
};

export const register = async (email: string, password: string, hcaptcha: string) => {
    return api.post('/api/v1/user/register', { email, password, hcaptcha });
};

export const refresh = async (refresh: string) => {
    return api.post('/api/v1/user/refresh', { refresh });
};

export const getUserInfo = async () => {
    return api.get('/api/v1/user/self');
};

export const editUserInfo = async (user : {}) => {
    return api.put('/api/v1/user/self', {...user});
};

export const getUserSessions = async (page: number) => {
    return api.get('/api/v1/user/sessions', { params: { page } });
}

export const removeSession = async (session_time: string) => {
    return api.post("/api/v1/user/remove_session", { session_time });
}