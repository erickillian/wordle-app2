import { ref, watch, onMounted } from "vue";

export function usePaginatedSearch<T>(
    fetchData: (search: string, page: number) => Promise<any>, // Accepts a generic fetch function
) {
    const searchQuery = ref("");
    const items = ref<T[]>([]);
    const loading = ref(false);
    const error = ref(false);

    const page = ref({
        current_page: 1,
        total_pages: 1,
        page_size: 20,
        count: 0,
        has_next: false,
        has_prev: false,
    });

    const getSearchItems = async (search: string, page_num: number) => {
        loading.value = true;
        error.value = false;
        try {
            const response = await fetchData(search, page_num);
            items.value = response.data.results;
            page.value = {
                current_page: response.data.page.current_page,
                total_pages: response.data.page.total_pages,
                page_size: response.data.page.page_size,
                count: response.data.page.count,
                has_next: response.data.page.has_next,
                has_prev: response.data.page.has_prev,
            };
        } catch {
            error.value = true;
            items.value = [];
        } finally {
            loading.value = false;
        }
    };

    const onPageUpdate = (newPage: number) => {
        getSearchItems(searchQuery.value, newPage);
    };

    // Watch search input
    watch(searchQuery, (newSearch) => {
        page.value.current_page = 1;
        getSearchItems(newSearch, page.value.current_page);
    });

    // Initial fetch
    onMounted(() => {
        getSearchItems(searchQuery.value, page.value.current_page);
    });

    return {
        searchQuery,
        items,
        loading,
        error,
        page,
        onPageUpdate,
        getSearchItems,
    };
}
