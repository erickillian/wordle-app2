
export interface User {
    slug: string;
    display_name: string;
    color_mode: string;
};

export interface Page {
    count: number;
    current_page: number;
    has_next: boolean;
    has_prev: boolean;
    page_size: number;
    total_pages: number;
};

export interface ActiveWordle {
    slug: string;
    start_time: string;
    solved: boolean;
    guess_history: string;
    guesses: number;
    correct: boolean;
};

export interface FinishedWordle {
    slug: string;
    start_time: string;
    time: string;
    solved: boolean;
    guess_history: string;
    guesses: number;
    correct: string;
    word: string;
};
