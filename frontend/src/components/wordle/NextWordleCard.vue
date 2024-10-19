<template>
    <v-card>
        <v-card-subtitle style="margin-top: 10px; margin-bottom: 10px">
            Time Until Next Wordle: {{ timeUntilNextWordle }}
        </v-card-subtitle>
    </v-card>
</template>

<script>
export default {
    name: 'NextWordleCard',
    data() {
        return {
            currentTime: new Date()
        };
    },
    computed: {
        timeUntilNextWordle() {
            const now = this.currentTime;
            const nextDay = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + 1));
            const diff = nextDay - now;
            const hours = Math.floor(diff / 3600000);
            const minutes = Math.floor((diff % 3600000) / 60000);
            const seconds = Math.floor((diff % 60000) / 1000);
            return `${hours}h ${minutes}m ${seconds}s`;
        }
    },
    mounted() {
        this.updateTime();
        this.interval = setInterval(this.updateTime, 1000);
    },
    beforeDestroy() {
        clearInterval(this.interval);
    },
    methods: {
        updateTime() {
            this.currentTime = new Date();
        }
    }
};
</script>

<style scoped>

</style>
