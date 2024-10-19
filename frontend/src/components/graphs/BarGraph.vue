<template>
    <div class="bar-graph-container">
        <Bar :data="barGraphData" :options="barGraphOptions" />
    </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { defineComponent, computed } from 'vue'
import { useTheme } from 'vuetify'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default defineComponent({
    name: 'BarGraph',
    components: { Bar },
    props: {
        keys: {
            type: Array,
            default: () => []
        },
        values: {
            type: Array,
            default: () => []
        }
    },
    setup(props) {
        const theme = useTheme();
        const barGraphData = computed(() => ({
            labels: props.keys,
            datasets: [{
                label: 'Number of guesses',
                backgroundColor: theme.current.value.colors.primary,
                data: props.values,
            }]
        }));

        const barGraphOptions = {
            responsive: true,
            maintainAspectRatio: false,
            // animation: {
            //     duration: 0 // Disable animation
            // },
            plugins: {
            legend: { display: false }
            },
            scales: {
            x: { grid: { display: false } },
            y: { grid: { display: false } }
            }
        };

        return { barGraphData, barGraphOptions }
    }
})
</script>

<style scoped>
.bar-graph-container {
    width: 100%;
    height: 100%;
}
</style>
