<template>
  <div class="order-core animated fadeIn">
     <v-layout class='order-layout'>
         <div class='create-order'>
             <v-btn large @click='newOrder()' rounded color='#1976d2' class='mr-5'>New Order</v-btn>
         </div>

         <div class='flex-container'>
             <v-flex xs12 sm12 md9 lg9 xl9 class='orders-flex'>
                 <v-tabs
                    v-model="tab"
                    background-color="white"
                    dark
                    slider-color='#15141c'
                >
                    <v-tab class='ml-5'>
                        <p style='color:#15141c;font-size: 17px;text-transform:capitalize;font-weight:bold'>
                            <v-icon style='font-size: 30px;' color='#15141c'>fas fa-truck-loading</v-icon>
                            Orders
                        </p>
                    </v-tab>
                    <v-tab class='ml-5'>
                        <p style='color:#15141c;font-size: 17px;text-transform:capitalize;font-weight:bold'>
                            <v-icon  style='font-size: 30px;' color='#15141c'>fas fa-coins</v-icon>
                            Payments
                        </p>
                    </v-tab>
                </v-tabs>

                <v-tabs-items v-model='tab'>
                    <v-tab-item v-if='orders[0].count > 0' style='width: 1000px;margin-top:50px;' class='ml-5'>
                        <OrdersTemp :orderArr='orders'/>
                    </v-tab-item>
                    <v-tab-item v-else>
                        <div class='no-orders' style='width: 900px;margin-top:50px;'>
                            <v-icon>fas fa-truck-loading</v-icon>
                            <p class='mt-3'>No Orders</p>
                        </div>
                    </v-tab-item>
                     
                    <v-tab-item style='width: 970px;margin-top:50px;' class='ml-5'>
                        <div  class='payment-container' v-if='customerPayments[0].count > 0'>
                            <div class='payments mt-5 ml-5 animated fadeInUp' 
                                v-for="(payment, i) in customerPayments[0].payments" 
                                :key='i'
                                @click='$store.state.infoDrawer=true, paymentDetails(payment.customer[0].id)'
                            >
                                <p>
                                    <v-icon class='mr-2' color='#15141c'>fas fa-user-circle</v-icon>
                                    <span>{{payment.customer[0].name}}</span>
                                    <span class='ml-3'>({{payment.payment_interval}})</span>
                                </p>

                                <p style='position: relative;top:5px;margin-left:60px' class=''>
                                    <v-icon style='font-size: 20px' color='#15141c'>fas fa-credit-card</v-icon>
                                    {{payment.methods[0].name}}
                                </p>
                                
                                <PaymentProgressBar 
                                    class='ml-3'
                                    style='position: relative;top:3px;'
                                    :times="payment.times"
                                    :paymentDatesArr="payment.payment_dates"
                                />
                            </div>
                        </div>
                        <div class='no-payments' v-else>
                            <v-icon>fas fa-coins</v-icon>
                            <p class='mt-3'>No payment scheduled </p>
                        </div>
                    </v-tab-item>
                </v-tabs-items>
            </v-flex>

            <v-flex xs12 sm12 md3 lg3 xl3 class='calendar-flex mt-5 mr-5'>
                <Calendar 
                    @orders='getOrders'
                    @payments='getPayments'
                />
            </v-flex>
         </div>
     </v-layout>
     <InformationModal 
            bColor='#15141c'    
            border='1px solid #15141c'
            closeClr='white' 
    />
  </div>
</template>

<script>
import InformationModal from "@/components/modals/InformationModal.vue";
import PaymentProgressBar from "@/components/layouts/PaymentProgressBar.vue";
import OrdersTemp from "@/components/layouts/OrdersTemp.vue";
import Calendar from "@/components/layouts/Calendar.vue";
import { mapGetters } from 'vuex';
export default {
  name: "Order",
  
  components: {
        PaymentProgressBar,
        OrdersTemp,
        InformationModal,
        Calendar,
        // PaymentProgressBar
    },

    computed: {
        ...mapGetters({
            // orders
            orders: 'order/getOrders',
            customerPayments: 'order/getPayments',
        }),
    },


  data(){
    return{
      tab: null,
    }
  },

  created(){
    this.getOrders(null)
    this.allPayments(0)
    console.log( this.customerPayments.payments);
    this.customerPayments[0].payments.forEach((items) => {
        console.log(items);
    })
  },

  methods: {
        getOrders(date){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "order/orders",
                params: {
                    date: date,
                    limit: 0,
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log('orders',data);
                    store.getters["setData"]([store.state.order.ordersArr, [data]]);
                },
            });
        },

        allPayments(limit){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "order/payments",
                params: {
                    limit: limit,
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log('payments',data);
                    store.getters["setData"]([store.state.order.paymentsArr, [data]]);
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

        newOrder(){
            this.$store.state.formsDialog = true;
            this.$store.state.formName = 'Order';
            this.$store.state.formsTemp = 'OrderStepper';
        }
  }
};
</script>

<style scoped>
  .order-core{
        height: auto;
        width: 85%;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        margin-left: 15%;
        /* background-color: #1e1d2b; */
        background-color: #fafafa;
    }
    .order-layout{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: flex-start;
        padding-top: 30px;
    }
    .create-order{
        width: 100%;
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
    }
    .create-order .v-btn{
        color: #fff;
        font-size: 15px;
        font-weight: bolder;
        text-transform: capitalize;
    }
    .flex-container{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: flex-start;
    }
    .orders-flex{
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .v-window__container{
        width: 100%;
    }
    .v-tabs {
        width: 100%;
        height: auto;
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .v-tabs-items{
        width: 100%;
        height: auto;
        min-height: 80vh;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    /* .v-tab-item{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        border: 1px solid green;
    } */
   .calendar-flex{
        height: auto;
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
    }
    .no-orders{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height:80vh;
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
     .payment-container{
        width: 100%;
        height:auto;
        /* background-color: #15141c; */
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content:flex-start;
        align-items: flex-start;
    }
    .payment-container .payments{
        width: 100%;
        height:60px;
        display: flex;
        flex-direction: row;
        justify-content:flex-start;
        align-items: flex-start;
        cursor: pointer;
        border: 1px solid #fafafa;
        border-radius: 10px;
        background-color: #ebf0f7;
        /* padding: 10px 10px 0px 10px; */
        padding-top: 10px;
        padding-left: 20px;
        padding-bottom: 0px;
        margin-bottom: -5px;
        cursor: pointer;
        box-shadow: rgba(255, 255, 255, 0.2) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0.9) 0px 0px 0px 1px;
        /* box-shadow: 5px 11px 15px -7px rgba(0, 0, 0, 0.2), 0px 24px 38px 3px rgba(0, 0, 0, 0.14), 0px 9px 46px 8px rgba(0, 0, 0, 0.12); */
    }
    .payment-container .payments .v-icon{
        font-size: 40px;
    }
    .payment-container .payments p{
        font-size: 15px;
        color: #15141c;
        font-weight: bold;
        text-align: left;
    }
    .payment-container .no-payments{
        width: 100%;
        height:450px;
        background-color: #15141c;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content:center;
        align-items: center;
    }
    .payment-container .no-payments .v-icon{
        font-size: 70px;
        color: #1e1d2b;
    }
    .payment-container .no-payments p{
        text-align: center;
        color: #1e1d2b;
        font-size: 15px;
        font-weight: bold;
    }
</style>
