<template>
    <v-card max-width="300">
        <v-card-title class="text-center time-clock">
            {{ formattedTime }}
        </v-card-title>
    </v-card>
</template>

<script>
export default {
    name: 'TimeClockComponent',
    props: {
        startTime: {
            type: String,
            default: null
        },
        elapsedTime: {
            type: String,
            default: null
        }
    },
    data() {
        return {
            currentTime: new Date(),
            timer: null
        };
    },
    computed: {
        hasEnded() {
            return this.elapsedTime && this.elapsedTime !== '';
        },
        formattedTime() {
            if (this.hasEnded) {
                // Elapsed time format: HH:MM:SS.MMMMMM
                const [hours, minutes, seconds] = this.elapsedTime.split(':');
                let [wholeSeconds, microseconds] = seconds.split('.');
                if (microseconds === undefined) {
                    microseconds = '000'; // Default to '000' if microseconds are not provided
                }
                const milliseconds = microseconds.substring(0, 3); // Only show milliseconds

                return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}:${wholeSeconds.padStart(2, '0')}.${milliseconds.padStart(3, '0')}`;
            }

            if (!this.startTime) {
                return '00:00:00.000';
            }

            const start = new Date(this.startTime);
            const now = this.currentTime;
            const elapsed = new Date(now - start);
            const hours = String(elapsed.getUTCHours()).padStart(2, '0');
            const minutes = String(elapsed.getUTCMinutes()).padStart(2, '0');
            const seconds = String(elapsed.getUTCSeconds()).padStart(2, '0');
            const milliseconds = String(elapsed.getUTCMilliseconds()).padStart(3, '0');

            return `${hours}:${minutes}:${seconds}.${milliseconds}`;
        }
    },
    watch: {
        startTime(newVal, oldVal) {
            this.handleTimerChange();
        },
        elapsedTime(newVal, oldVal) {
            this.handleTimerChange();
        }
    },
    methods: {
        handleTimerChange() {
            if (this.hasEnded) {
                // If the timer has ended, clear the interval
                if (this.timer) {
                    clearInterval(this.timer);
                    this.timer = null;
                }
            } else if (this.startTime) {
                // If the timer hasn't ended and startTime exists, start the timer
                if (!this.timer) {
                    this.timer = setInterval(() => {
                        this.currentTime = new Date();
                    }, 1); // Update every 100ms
                }
            } else {
                // No startTime, reset the timer to 0
                if (this.timer) {
                    clearInterval(this.timer);
                    this.timer = null;
                }
                this.currentTime = new Date(0);
            }
        }
    },
    mounted() {
        this.handleTimerChange(); // Initialize timer on mount
    },
    beforeDestroy() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    }
};
</script>

<style scoped>
.time-clock {
    font-size: 2rem;
    font-family: 'Courier New', Courier, monospace;
}
</style>
