<template>
    <div class="bar-graph-container">
        <canvas ref="barGraphCanvas"></canvas>
    </div>
</template>

<script>
import { Chart as ChartJS, BarController, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { defineComponent, onMounted, onUnmounted, ref, computed, watch } from 'vue';
import { useTheme } from 'vuetify';

// Register all required components, including BarController
ChartJS.register(BarController, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default defineComponent({
    name: 'BarGraph',
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
        const barGraphCanvas = ref(null);
        let barChartInstance = null;

        const barGraphData = computed(() => ({
            labels: props.keys,
            datasets: [{
                label: 'Number of wordles',
                backgroundColor: theme.current.value.colors.primary,
                data: props.values,
            }]
        }));

        const barGraphOptions = {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 400
            },
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { grid: { display: false } },
                y: { grid: { display: false } }
            }
        };

        onMounted(() => {
            if (barGraphCanvas.value) {
                barChartInstance = new ChartJS(barGraphCanvas.value, {
                    type: 'bar',
                    data: barGraphData.value,
                    options: barGraphOptions
                });
            }
        });

        watch([() => props.keys, () => props.values], () => {
            if (barChartInstance) {
                barChartInstance.data.labels = props.keys;
                barChartInstance.data.datasets[0].data = props.values;
                barChartInstance.update(); // Update the chart to reflect the new data
            }
        });

        onUnmounted(() => {
            if (barChartInstance) {
                barChartInstance.destroy();
            }
        });

        return { barGraphCanvas }
    }
});
</script>

<style scoped>
.bar-graph-container {
    width: 100%;
    height: auto;
    position: relative;
    padding-bottom: 50%;
    /* Adjust this value to maintain the aspect ratio */
    max-height: 500px;
    /* Example max-height, adjust as necessary */
}

.bar-graph-container canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
</style>
