<template>
    <div class='dash-core animated fadeIn pb-5' v-if="this.$session.has('authenticated') && this.$session.get('authenticated')">
        <div class='claendar-ctrl mt-5 hidden-sm-and-down' style='display:flex;justify-content:flex-end;align-items:center;width:97%;'>
            <v-btn
                class="font-weight-bold"
                large
                color="#1976d2"
                style='cursor:pointer;text-transform:capitalize'
                rounded
                @click='$store.state.calendarStatus = !$store.state.calendarStatus'
            >
                <v-icon left style='font-size:20px;' class='pl-2 pt-2 pb-2' color='white'>
                    fas fa-calendar-alt
                </v-icon>
                <span v-if='$store.state.calendarStatus' style='color:white;'>Hide Calendar</span>
                <span v-else style='color:white;'>Show Calendar</span>
            </v-btn>
        </div>
        <v-layout class="dash-layout">

            <v-flex xs12 sm12 md8 lg8 xl8 class='left-side'>
                <div class='counts'>
                    <v-flex xs12 sm12 md4 lg4 xl4 class='products-count'>
                        <div class='inventory-header'>
                            <v-icon style='font-size: 30px;' class='mb-2 ml-3'>fas fa-boxes</v-icon>
                            <p class='ml-3'>Inventory</p>
                        </div>

                        <div class='inventory-container'>
                            <h1 class='display-3 animated bounceIn'>{{products[0].count}}</h1>
                        </div>
                    </v-flex>
                    
                    <!-- <v-flex xs12 sm12 md4 lg4 xl4 class='incoming-counts'>
                        <p>
                                Incoming products
                        </p>
                        <v-icon style='font-size: 70px;' class='mb-3'>fas fa-boxes</v-icon>
                        <h1 class='display-3 animated bounceIn'>{{addedProducts[0].count}}</h1>
                    </v-flex> -->
                    <v-flex xs12 sm12 md4 lg4 xl4 class='paying-counts'>
                            <div class='payment-header'>
                                <v-icon>fas fa-coins</v-icon>
                                <p class='mt-1 ml-3'>Payments</p>
                            </div>
                            <div class='count-container'>
                                <h1 class='display-3 animated bounceIn'>{{customerPayments[0].count}}</h1>
                            </div>
                    </v-flex>

                    <v-flex xs12 sm12 md3 lg3 xl3 class='orders-count'>
                            <div class='order-header'>
                                <v-icon>fas fa-truck-loading</v-icon>
                                <p class='animated bounceIn ml-3'>Orders</p>
                            </div>
                            <div class='order-container'>
                                <h1 class='display-3 animated bounceIn'>{{orders[0].count}}</h1>
                            </div>
                    </v-flex>
                </div>

                <div class="orders" v-if='orders[0].count > 0'>
                    <div class='orders-header' style='margin-left:2%;'>
                        <p>
                            <v-icon color='#1e1d2b' medium>fas fa-truck-loading</v-icon>
                            <span>Orders</span>
                        </p>
                    </div>
                    <OrdersTemp :orderArr='orders'/>
                </div>
                <div class='no-orders' v-else>
                    <v-icon>fas fa-truck-loading</v-icon>
                    <p class='mt-3'>No Sales</p>
                </div>
            </v-flex>

            <v-flex xs12 sm12 md3 lg3 xl3 class='rigth-side'>
                <div class='calendar-payments'>
                    <div class='calendar hidden-sm-and-down' v-if='$store.state.calendarStatus'>
                        <Calendar 
                            @orders='getOrders'
                            @payments='getPayments'
                            @addedProducts='getAddedProducts'
                        />
                    </div>

                    <div  class='payment-container' v-if='customerPayments[0].count > 0'>
                        <div class='payment-header'>
                            <p>
                                <v-icon color='#15141c' medium>fas fa-coins</v-icon>
                                <span>Schedulded Pyaments</span>
                            </p>
                        </div>
                        <div class='payments mt-5 ml-5 animated fadeInUp' 
                            v-for="(payment, i) in customerPayments[0].payments" 
                            :key='i'
                            @click='$store.state.infoDrawer=true, paymentDetails(payment.id)'
                        >
                            <v-flex xs12 sm12 md7 lg7 xl7>
                                <p class='user-info'>
                                    <v-icon class='mr-2' color='#1e1d2b'>fas fa-user-circle</v-icon>
                                    <span>{{payment.customer[0].name}}</span>
                                    <span class='ml-3'>({{payment.payment_interval}})</span>
                                </p>
                            </v-flex>
                            <v-flex xs12 sm12 md5 lg5 xl5>
                                <PaymentProgressBar 
                                    class='ml-3'
                                    style='position: relative;top:3px;'
                                    width='70%'
                                    :times="payment.times"
                                    :paymentDatesArr="payment.payment_dates"
                                />
                            </v-flex>
                        </div>
                    </div>
                    <div class='no-payments' v-else>
                        <v-icon>fas fa-coins</v-icon>
                        <p class='mt-3'>No payment scheduled for {{paymentDate}} </p>
                    </div>
                </div>
            </v-flex>
        </v-layout>
        <InformationModal 
            bColor='#15141c'    
            border='1px solid #15141c'
            closeClr='white' 
        />
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import PaymentProgressBar from "@/components/layouts/PaymentProgressBar.vue";
import OrdersTemp from "@/components/layouts/OrdersTemp.vue";
import InformationModal from "@/components/modals/InformationModal.vue";
import Calendar from "@/components/layouts/Calendar.vue";
export default {
    name: 'Dashboard',

    components: {
        PaymentProgressBar,
        OrdersTemp,
        InformationModal,
        Calendar,
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
            paymentDate: 'today',
            page: 1,
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
        this.getAddedProducts(null)
        // orders
        this.getPayments(null)
        this.getOrders(null)
        this.$store.state.infoDrawer = false
    },

    methods: {
        allProducts(){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/products",
                params: {
                    date: null,
                    user_id: Number(this.$session.get('warehouseId'))==this.$session.get('userId') ? 0 : this.$session.get('warehouseId')
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log(data);
                    store.getters["setData"]([store.state.product.productsArr, [data]]);
                },
            });
        },

        getAddedProducts(date){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/come_in",
                params: {
                    date: date
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log('added',data);
                    store.getters["setData"]([store.state.product.addedProductsArr, [data]]);
                },
            });
        },

        getPayments(date){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "order/ongoing_payments",
                params: {
                    date: date,
                    limit: 0,
                    user_id: this.$session.get('warehouseId'),
                    su_id: this.$session.get('userId'),
                    pagination: self.page,
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log('payments',data);
                    store.getters["setData"]([store.state.order.paymentsArr, [data]]);
                },
            });
        },

        paymentDetails(customerid){
            let self = this;

            this.$store.dispatch('order/getPaymentDetails', {
                url: 'order/payment_details',
                params: {
                    customerId: customerid
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data){
                    // console.log('api data', data);
                    self.$store.state.infoTempName = 'PaymentDetails'
                    self.$store.getters["setData"]([self.$store.state.order.customerPaymentArr, [data]]);
                    
                },
            })
        },

        getOrders(date){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "order/orders",
                params: {
                    date: date,
                    limit: null,
                    user_id: this.$session.get('warehouseId'),
                    pagination: self.page,
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
        min-height: 100vh;
        height: auto;
        width: auto;
        display: flex;
        flex-direction:column;
        justify-content: center;
        align-items: flex-start;
        margin-left: 15%;
        /* background-color: #1e1d2b; */
        background-color: #fff;
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
        /* background-color: #15141c; */
        background-color: #ebf0f7;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 2px 6px 2px;
        /* box-shadow: 5px 11px 15px -7px rgba(0, 0, 0, 0.2), 0px 24px 38px 3px rgba(0, 0, 0, 0.14), 0px 9px 46px 8px rgba(0, 0, 0, 0.12); */
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
        height:300px;
        background-color: #ebf0f7;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 2px 6px 2px;
        border-radius: 10px;
    }
    .order-header, .payment-header, .inventory-header{
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
        margin-left: 30px;
    }
    .paying-counts .count-container, .orders-count .order-container, .inventory-container{
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
         height: 70%;
    }
    .products-count p, .incoming-counts p, .orders-count p, .paying-counts p{
        color: #15141c;
        /* color: #1e1d2b; */
        font-size: 18px;
        font-weight: bold;
        text-align: left;
    }
    .products-count h1, .incoming-counts h1, .orders-count h1, .paying-counts h1{
        color: #15141c;
        /* color: #1e1d2b; */
        text-align: center;
        font-weight: bold;
    }
    .counts .v-icon{
        /* color: #0163d1; */
        color: #15141c;
        font-size: 30px;
    }
    .orders{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        margin-top: 30px;
        height:550px;
        background-color: #ebf0f7;
        box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
        border-radius: 10px;
        overflow-y: scroll;
        overflow-x: hidden;
    }
    .no-orders{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-top: 30px;
        height:550px;
        background-color: #ebf0f7;
        box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
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
        background-color: #ebf0f7;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 2px 6px 2px;
        border-radius: 10px;
    }
    .payment-container{
        width: 100%;
        height:450px;
        background-color: #ebf0f7;
        box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content:flex-start;
        align-items: flex-start;
        overflow-y: scroll;
        overflow-x: hidden;
    }
    ::-webkit-scrollbar {
         width: 10px;
    }
    .payment-header, .orders-header{
        width: 90%;
        height: auto;
        margin-left: 5%;
        margin-top: 20px;
        margin-bottom: 10px;
        display: flex;
        justify-content: flex-start;
        align-items: flex-end;
    }
    .payment-header p, .orders-header p{
        margin: 0px;
        padding: 0px;
    }
    .payment-header p span, .orders-header p span{
        color: #1e1d2b;
        font-weight: bold;
        margin-left: 10px;
    }
    .calendar-payments .payments{
        width: 100%;
        height:auto;
        display: flex;
        flex-direction: row;
        justify-content:flex-start;
        align-items: flex-start;
        cursor: pointer;
    }
    .calendar-payments .payments .v-icon{
        font-size: 40px;
    }
    .calendar-payments .payments p{
        font-size: 15px;
        color: #1e1d2b;
        font-weight: bold;
        text-align: left;
    }
    .calendar-payments .no-payments{
        width: 100%;
        height:450px;
        background-color: #ebf0f7;
        box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
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
    @media only screen and (max-width: 1500px) {
        /* .dash-core{
            margin-left: 20%;
        } */
        .user-info{
            display: flex;
            flex-direction: column;
            justify-content:center;
            align-items: center;
        }
    }
    @media only screen and (max-width: 500px) {
        .dash-core{
            margin-left: 0%;
            align-items: center;
        }
        .dash-layout{
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding-top: 50px;
            /* width: 90%; */
        }
        .left-side, .rigth-side{
            align-items: center;
        }
        .counts{
            justify-content: flex-start;
            padding-right: 10px;
            align-items: flex-start;
            overflow-x: scroll;
        }
        .products-count, .paying-counts, .orders-count{
            margin-left:20px;
            margin-right:20px;
            padding-left:65px;
            padding-right:65px;
        }
        .orders, .no-orders, .payment-container{
            width: 90%;
            
             align-items: center;
        }
        .payment-container{
            margin-top: 50px;
            margin-left: 5%;
        }
    }
</style>