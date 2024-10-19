import api from './api';

// Function to fetch the list of users with pagination
export const fetchUsers = async (search: string, page: number) => {
    return await api.get('/api/v1/user/users', { params: { search, page } });
};
