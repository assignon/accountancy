<template>
    <div class='order-temp-core'>
        <v-layout class='order-temp-layout'>
            <v-flex xs12 sm12 md2 lg2 xl2 class='customer-name'>
                <v-icon medium>fas fa-</v-icon>
                <p>{{}}</p>
            </v-flex>

            <v-flex xs12 sm12 md3 lg3 xl3 class='product-name'>
                <p>{{}} <span>({{}})</span></p>
                <p>+{{}}</p>
            </v-flex>

            <v-flex xs12 sm12 md3 lg3 xl3 class='date'>
                <p>{{}}</p>
            </v-flex>

            <v-flex xs12 sm12 md2 lg2 xl2 class='price'>
                <p>{{}}</p>
            </v-flex>

            <v-flex xs12 sm12 md2 lg2 xl2 class='payment-method'>
                <p>{{}}</p>
            </v-flex>

        </v-layout>
    </div>
</template>

<script>
export default {
    name: 'OrderTemp',

    props:[],

    computed: {},

    data(){
        return{

        }
    },

    methods: {

    }
}
</script>

<style scoped>
    .order-temp-core{
        height: auto;
        width: 85%;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        margin-left: 15%;
        border: 1px solid #1e1d2b;
        border-radius: 15px;
        background-color: #1e1d2b;
        padding: 30px;
    }
    .order-temp-layout{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
    }
   
</style>