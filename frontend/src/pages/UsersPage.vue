<template>
    <v-row dense class="mx-0">
        <v-navigation-drawer app :clipped="true" width="500" v-model="showSider" elevation="0">
            <UsersSearchComponent :onUserSelected="onUserSelect" :selectedUserSlug="selectedUser" />
        </v-navigation-drawer>
        <v-col>
            <v-container fluid class="pa-4">
                <template v-if="selectedUser">
                    <UserViewComponent :slug="selectedUser" />
                </template>
                <template v-else>
                    <v-alert color="primary" type="info" class="mt-4">
                        Please select a user to view their information.
                    </v-alert>
                </template>
            </v-container>
        </v-col>
        <v-fab class="d-xs-flex d-sm-flex d-lg-none rounded-circle" location="bottom right" size="64" absolute app
            color="primary" @click="toggleSider" rounded="circle">
            <v-icon>mdi-account</v-icon>
        </v-fab>
    </v-row>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import UsersSearchComponent from '@/components/UsersSearchComponent.vue';
import UserViewComponent from '@/components/UserViewComponent.vue';
import { useRouter } from 'vue-router';
import { useDisplay } from 'vuetify';

export default defineComponent({
    name: 'PlayersView',
    components: {
        UsersSearchComponent,
        UserViewComponent
    },
    props: {
        slug: {
            type: String,
            required: false
        }
    },
    setup(props) {
        const router = useRouter();
        const selectedUser = ref<string>('');
        const showSider = ref<boolean>(true);

        watch(() => props.slug, (slug: string | undefined): void => {
            if (slug !== undefined) {
                selectedUser.value = slug;
            } else {
                selectedUser.value = '';
            }
        });
        

        onMounted((): void => {
            if (props.slug !== undefined) {
                selectedUser.value = props.slug;
                
                const { xs, sm, md } = useDisplay();
                if (xs.value || sm.value || md.value) {
                    showSider.value = false;
                }
            }
        });

        const onUserSelect = (slug: string): void => {
            if (slug !== '') {
                router.push(`/users/${slug}`);
                selectedUser.value = slug;
            } else {
                router.push('/users');
                selectedUser.value = '';
            }
        };

        const toggleSider = (): void => {
            showSider.value = !showSider.value;
        };

        return {
            selectedUser,
            showSider,
            onUserSelect,
            toggleSider,
        };
    }
});
</script>

<style scoped></style>
