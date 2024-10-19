<template>
    <v-app>
        <!-- Header -->
        <v-app-bar app :elevation="0">
            <v-toolbar-title></v-toolbar-title>
            <v-spacer></v-spacer>
            <v-tooltip location="bottom" v-model="tooltipVisible" class="bounce">
                <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" @click="goToLogin">Login</v-btn>
                </template>
                <template v-slot:default>
                    <div style="display: flex; align-items: center; flex-direction: column;">
                        <v-icon large>mdi-arrow-up-bold</v-icon>
                        <span style="font-weight: bold; font-size: 24px;">Login</span>
                    </div>
                </template>
            </v-tooltip>
            <v-btn @click="goToRegister">Register</v-btn>
        </v-app-bar>

        <!-- Main Content -->
        <v-main app>
            <v-container>

                <v-row justify="center">
                    <v-col cols="12" class="text-center">
                        <h1 class="display-1 font-weight-bold" style="font-size: 10vw;">Wordle</h1>
                        <p class="subtitle-1" style="font-size: 2vw;">A competitive web app that allows users to play
                            and compete at wordle each day.</p>
                        <v-card class="rounded-lg mx-auto mt-10" max-width="1080" style="padding-bottom: 0;">
                            <video autoplay loop muted playsinline style="width: 100%; height: auto; display: block;">
                                <source src="@/assets/wordle_promo_video.mp4" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </v-card>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="12">
                        <TestWordleComponent />
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
        <v-footer :elevation="0" absolute>
            <v-container>
                <v-row>
                    <v-col class="text-center">
                        <p>© {{ new Date().getFullYear() }} All rights reserved to Eric Killian :p.</p>
                    </v-col>
                </v-row>
            </v-container>
        </v-footer>
    </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import TestWordleComponent from '@/components/wordle/TestWordleComponent.vue';

export default defineComponent({
    name: 'HomePage',
    components: {
        TestWordleComponent,
    },
    data() {
        return {
            tooltipVisible: true,
            isBouncing: false,
            startBouncing() {
                this.isBouncing = true;
            },
            stopBouncing() {
                this.isBouncing = false;
            }
        };
    },
    setup() {
        const router = useRouter();

        const goToLogin = () => {
            router.push('/login');
        };

        const goToRegister = () => {
            router.push('/register');
        };

        return {
            goToLogin,
            goToRegister,
        };
    },
});
</script>

<style scoped>
.fill-height {
    height: 100vh;
}

.bounce {
    animation: bounce 1s infinite;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-15px);
    }
    60% {
        transform: translateY(-7.5px);
    }
}
</style>