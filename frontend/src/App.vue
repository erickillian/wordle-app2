<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import { defineComponent, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from 'vuetify'

export default defineComponent({
  setup() {
    const authStore = useAuthStore()
    const theme = useTheme()

    const updateTheme = (newColorMode) => {
        if (newColorMode) {
            theme.global.name.value = newColorMode
        }
    }

    onMounted(() => {
        updateTheme(authStore.user?.color_mode)
    })
  }
})
</script>
