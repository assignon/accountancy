<template>
    <div class='dash-core animated fadeIn' v-if="this.$session.has('authenticated') && this.$session.get('authenticated')">
        <v-layout class="dash-layout">

            <v-flex xs12 sm12 md8 lg8 xl8 class='left-side'>
                <div class='counts'>
                    <v-flex xs12 sm12 md4 lg4 xl4 class='products-count'>
                        <p>
                            All products
                        </p>
                        
                        <v-icon style='font-size: 70px;' class='mb-3'>fas fa-boxes</v-icon>
                        <h1 class='display-3'>{{products[0].count}}</h1>
                    </v-flex>
                    
                    <v-flex xs12 sm12 md4 lg4 xl4 class='incoming-counts'>
                        <p>
                                Incoming products
                        </p>
                        <v-icon style='font-size: 70px;' class='mb-3'>fas fa-boxes</v-icon>
                        <h1 class='display-3'>{{addedProducts[0].count}}</h1>
                    </v-flex>

                    <v-flex xs12 sm12 md3 lg3 xl3 class='orders-payments'>
                        <div class='paying-counts'>
                            <div>
                                <v-icon>fas fa-coins</v-icon>
                                <p class='mt-3'>Payments</p>
                            </div>
                            <h3 class='display-1'>{{customerPayments[0].count}}</h3>
                        </div>

                        <div class='orders-count'>
                            <div>
                                <v-icon>fas fa-truck-loading</v-icon>
                                <p class='mt-3'>Orders</p>
                            </div>
                            <h3 class='display-1'>{{orders[0].count}}</h3>
                        </div>
                    </v-flex>
                </div>

                <div class="orders" v-if='orders[0].count > 0'>

                </div>
                <div class='no-orders' v-else>
                    <v-icon>fas fa-truck-loading</v-icon>
                    <p class='mt-3'>No Orders</p>
                </div>
            </v-flex>

            <v-flex xs12 sm12 md3 lg3 xl3 class='rigth-side'>
                <div class='calendar-payments'>
                    <div class='calendar'></div>

                    <div  class='payment-container' v-if='customerPayments[0].count > 0'>
                        <div class='payment-header'>
                            <p>
                                <v-icon color='white' medium>fas fa-coins</v-icon>
                                <span>Pyaments for {{paymentDate}}</span>
                            </p>
                        </div>
                        <div class='payments mt-5 ml-5' 
                            v-for="(payment, i) in customerPayments" 
                            :key='i'
                        >
                            <p>
                                <v-icon class='mr-2' color='white'>fas fa-user-circle</v-icon>
                                <span>{{payment.customers[i].name}}</span>
                                <span class='ml-3'>({{payment.payments[i].payment_interval}})</span>
                            </p>
                            <!-- <p>{{ payment.payments[i].pay_in }}</p> -->
                            <PaymentProgressBar 
                                class='ml-3'
                                style='position: relative;top:3px;'
                                :times="payment.payments[i].times"
                                :paymentDatesArr="payment.payments[i].payment_dates"
                            />
                        </div>
                    </div>
                    <div class='no-payments' v-else>
                        <v-icon>fas fa-coins</v-icon>
                        <p class='mt-3'>No payment scheduled for {{paymentDate}} </p>
                    </div>
                </div>
            </v-flex>
        </v-layout>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import PaymentProgressBar from "@/components/layouts/PaymentProgressBar.vue";
export default {
    name: 'Dashboard',

    components: {
        PaymentProgressBar
    },

    computed: {
        ...mapGetters({
            // products
            products: 'product/getProducts',
            addedProducts: 'product/getAddedProducts',
            // orders
            orders: 'order/getOrders',
            customerPayments: 'order/getPayments',
        }),
    },

    data(){
        return {
            paymentDate: 'today'
        }
    },

    beforeCreate: function () {
        if(!this.$session.has('authenticated') | !this.$session.get('authenticated')) {
        this.$router.push({name: "Login"})
        }
    },

    created(){
        // products
        this.allProducts()
        this.getAddedProducts()
        // orders
        this.getPayments()
        this.getOrders()
    },

    methods: {
        allProducts(){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/products",
                params: {
                    date: null
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log(data);
                    store.getters["setData"]([store.state.product.productsArr, [data]]);
                },
            });
        },

        getAddedProducts(){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/come_in",
                params: {
                    date: null
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log('added',data);
                    store.getters["setData"]([store.state.product.addedProductsArr, [data]]);
                },
            });
        },

        getPayments(){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "order/ongoing_payments",
                params: {
                    date: '2021-01-22',
                    limit: 10,
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    console.log('payments',data);
                    store.getters["setData"]([store.state.order.paymentsArr, [data]]);
                },
            });
        },

        getOrders(){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "order/orders",
                params: {
                    date: '2021-01-22',
                    limit: 20,
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log('orders',data);
                    store.getters["setData"]([store.state.order.ordersArr, [data]]);
                },
            });
        }
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
        background-color: #1e1d2b;
    }
    .dash-layout{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: flex-start;
        padding-top: 50px;
    }
    .left-side{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
    }
    .counts{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
    }
    .products-count, .incoming-counts{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height:300px;
        background-color: #15141c;
        border-radius: 10px;
    }
    .orders-payments{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        height:300px;
    }
    .paying-counts, .orders-count{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height:149px;
        background-color: #15141c;
        border-radius: 10px;
    }
    .products-count p, .incoming-counts p, .orders-count p, .paying-counts p{
        color: white;
        /* color: #1e1d2b; */
        font-size: 18px;
        font-weight: bold;
        text-align: left;
    }
    .products-count h1, .incoming-counts h1, .orders-count h3, .paying-counts h3{
        color: white;
        /* color: #1e1d2b; */
        text-align: center;
        font-weight: bold;
    }
    .counts .v-icon{
        color: #0163d1;
        font-size: 30px;
    }
    .orders{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-top: 30px;
        height:550px;
        background-color: #15141c;
        border-radius: 10px;
    }
    .no-orders{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-top: 30px;
        height:550px;
        background-color: #15141c;
        border-radius: 10px;
    }
    .no-orders .v-icon{
        font-size: 100px;
        color: #1e1d2b;
    }
    .no-orders p{
        text-align: center;
        color: #1e1d2b;
        font-size: 20px;
        font-weight: bold;
    }
    .rigth-side{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
    }
    .calendar-payments{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .calendar-payments .calendar{
        height:400px;
        width: 100%;
        margin-bottom: 30px;
        background-color: #15141c;
        border-radius: 10px;
    }
    .payment-container{
        width: 100%;
        height:450px;
        background-color: #15141c;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content:flex-start;
        align-items: flex-start;
    }
    .payment-header{
        width: 90%;
        height: auto;
        margin-left: 5%;
        margin-top: 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: flex-start;
        align-items: flex-end;
    }
    .payment-header p{
        margin: 0px;
        padding: 0px;
    }
    .payment-header p span{
        color: white;
        margin-left: 10px;
    }
    .calendar-payments .payments{
        width: 100%;
        height:100%;
        display: flex;
        flex-direction: row;
        justify-content:flex-start;
        align-items: flex-start;
    }
    .calendar-payments .payments .v-icon{
        font-size: 40px;
    }
    .calendar-payments .payments p{
        font-size: 15px;
        color: white;
        font-weight: bold;
        text-align: left;
    }
    .calendar-payments .no-payments{
        width: 100%;
        height:450px;
        background-color: #15141c;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content:center;
        align-items: center;
    }
    .calendar-payments .no-payments .v-icon{
        font-size: 70px;
        color: #1e1d2b;
    }
    .calendar-payments .no-payments p{
        text-align: center;
        color: #1e1d2b;
        font-size: 15px;
        font-weight: bold;
    }
</style>