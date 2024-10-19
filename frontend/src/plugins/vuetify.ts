/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
// import { createApp } from 'vue'
import { createVuetify, type ThemeDefinition } from 'vuetify'



const mutualColors = {
    primary: '#2B8AEB',
    secondary: '#018786',
    error: '#B00020',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FB8C00',
}



const dark: ThemeDefinition = {
    dark: true,
    colors: {
        background: '#121212',
        surface: '#232323',
        text: '#FFFFFF',
        ...mutualColors,
    },
}


const light: ThemeDefinition = {
    dark: false,
    colors: {
        background: '#F1F1F1',
        surface: '#FFFFFF',
        text: '#000000',
        ...mutualColors,
    },
}

// Determine the default theme based on the user's color scheme preference
const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
const system = prefersDarkScheme ? dark : light;

export default createVuetify({
    theme: {
        defaultTheme: 'system',
        themes: {
            dark,
            light,
            system,
        },
    },
})
