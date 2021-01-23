<template>
    <div class='dash-core animated fadeIn' v-if="this.$session.has('authenticated') && this.$session.get('authenticated')">
        <v-layout class="dash-layout">

        </v-layout>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    name: 'Dashboard',

    components: {},

    computed: {
        ...mapGetters({

        }),
    },

    data(){
        return {

        }
    },

    beforeCreate: function () {
        if(!this.$session.has('authenticated') | !this.$session.get('authenticated')) {
        this.$router.push({name: "Login"})
        }
    },

    created(){
        
    },

    methods: {
        
    }
}
</script>

<style scoped>
    .dash-core{
        height: 100vh;
        width: 85%;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        margin-left: 15%;
        border: 1px solid red;
    }
</style>