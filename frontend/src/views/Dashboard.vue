<template>
    <div class='dash-core' v-if="this.$session.has('authenticated') && this.$session.get('authenticated')">
        <h1>welcom to the dash</h1>
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