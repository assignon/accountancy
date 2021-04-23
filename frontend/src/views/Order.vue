<template>
  <div class="order-core animated fadeIn">
     <v-layout class='order-layout'>
        <div class='create-order'>
            <div class='hide-serach-result' v-if='searchView==true'>
                <v-icon medium color='#15141c' @click='searchView=false'>fas fa-chevron-left</v-icon>
                <p style='color:#15141c; margin:auto' class='ml-3 font-weight-bold' @click='searchView=false'>Back</p>
            </div>
             <div class='order-search-form' ref='orderSearchForm'>
                <v-text-field
                    v-model="orderSearch"
                    label="Search Orders (e.g john)...*"
                    type='search'
                    rounded
                    required
                    filled
                    dense
                    append-icon="fas fa-search"
                    @keyup.enter='displaySearchView'
                    @input='searchOrder'
                ></v-text-field>
            </div>
            <!-- <v-btn large @click='newOrder()' rounded color='#1976d2' class='mr-5 hidden-sm-and-down'>New Sale</v-btn> -->
            <!-- calendar ctrl -->
            <v-btn
                class="mr-4 hidden-sm-and-down"
                large
                color="#1976d2"
                style='cursor:pointer'
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

        <div class='flex-container' v-if='!searchView'>
             <v-card  flat  width='100%' class='orders-flex'>
                 <v-tabs
                    v-model="tab"
                    background-color="white"
                    dark
                    slider-color='#15141c'
                >
                    <v-tab class='ml-5'>
                        <p style='color:#15141c;font-size: 17px;text-transform:capitalize;font-weight:bold'>
                            <v-icon style='font-size: 30px;' color='#15141c'>fas fa-truck-loading</v-icon>
                            Sales
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
                    <v-tab-item v-if='orders[0].count > 0' :style='{width: winWidth}' style='margin-top:50px;' class='ml-5'>
                        <v-flex xs9 sm9 md12 xl12 lg12 style='min-height:50vh'>
                            <OrdersTemp :orderArr='orders'/>
                        </v-flex>
                        <div class='pagination-container'>
                            <!-- <v-pagination
                                v-if='orders[0].count>$store.state.limit'
                                v-model="page"
                                :length="Math.ceil(orders[0].count/$store.state.limit)"
                                :total-visible="$store.state.totalVisible"
                                @input='getOrders(selectedDate)'
                            ></v-pagination> -->
                        </div>
                    </v-tab-item>
                    <v-tab-item v-else>
                        <div class='no-orders' style='width: 900px;margin-top:50px;'>
                            <v-icon>fas fa-truck-loading</v-icon>
                            <p class='mt-3'>No Sales</p>
                        </div>
                    </v-tab-item>
                     
                    <v-tab-item style='margin-top:50px;' :style='{width:tabWidth}' class='ml-5'>
                        <v-flex xs12 sm12 md8 lg10 xl12  class='payment-container' v-if='customerPayments[0].count > 0'>
                            <div class='payments mt-5 ml-5 animated fadeInUp' 
                                v-for="(payment, i) in customerPayments[0].payments" 
                                :key='i'
                                @click='$store.state.infoDrawer=true, paymentDetails(payment.id)'
                            >
                                <v-flex xs6 sm6 md4 lg4 xl4>
                                    <p>
                                        <v-icon class='mr-2' color='#15141c'>fas fa-user-circle</v-icon>
                                        <span>{{payment.customer[0].name}}</span>
                                        <span class='ml-3 hidden-sm-and-down'>({{payment.payment_interval}})</span>
                                    </p>
                                </v-flex>

                                <v-flex xs6 sm6 md3 lg3 xl3>
                                    <p style='position: relative;top:5px;margin-left:60px;text-align:left;' class=''>
                                        <v-icon style='font-size: 20px' class='hidden-sm-and-down' color='#15141c'>fas fa-credit-card</v-icon>
                                        {{payment.methods[0].name}}
                                    </p>
                                </v-flex>
                                
                                <PaymentProgressBar 
                                    class='ml-3 hidden-sm-and-down'
                                    style='position: relative;top:3px;'
                                    width='30%'
                                    :times="payment.times"
                                    :paymentDatesArr="payment.payment_dates"
                                />
                            </div>
                            <!-- ---------------------------------paginations ---------------------------------------------->
                            <!-- <v-pagination
                                v-if='customerPayments[0].count>$store.state.limit && !isAllPayments'
                                v-model="page"
                                :length="Math.ceil(customerPayments[0].count/$store.state.limit)"
                                :total-visible="$store.state.totalVisible"
                                @input='getPayments(selectedDate)'
                            ></v-pagination> -->
                            <!-- <v-pagination
                                v-if='customerPayments[0].count>$store.state.limit && isAllPayments'
                                v-model="page"
                                :length="Math.ceil(customerPayments[0].count/$store.state.limit)"
                                :total-visible="$store.state.totalVisible"
                                @input='allPayments($store.state.limit)'
                            ></v-pagination> -->
                        </v-flex>
                        <div class='no-payments' v-else>
                            <v-icon>fas fa-coins</v-icon>
                            <p class='mt-3'>No payment scheduled </p>
                        </div>
                    </v-tab-item>
                </v-tabs-items>
            </v-card>

            <v-flex xs12 sm12 md4 lg3 xl3 class='calendar-flex mt-5 mr-5' v-if='$store.state.calendarStatus'>
                <Calendar 
                    @orders='getOrders'
                    @payments='getPayments'
                />
            </v-flex>
        </div>
        <div class='order-search-result' v-else>
            <div class='order-founded' v-if='searchedOrder.length>0'>
                <OrdersTemp :orderArr='searchedOrder'/>
            </div>

            <div class='order-no-founded' v-if='searchedOrder.length==0'>
                <v-icon class='mb-3' style='font-size: 100px' color='#15141c'>fas fa-truck-loading</v-icon>
                <p class='font-weight-bold'>No order founded</p>
            </div>
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
            searchedOrder: 'order/getSearchedOrder',
        }),
    },


  data(){
    return{
      tab: null,
      orderSearch: null, //v-model
      searchView: false,
      tabWidth: window.innerWidth > 500 ? '100vh' : '400px',
      page: 1, // current pagination clicked number
      winWidth: window.innerWidth > 500 ? '100vh' : '450px',
      selectedDate: null,
      isAllPayments: true, // check if payments are fetch base on current date
    }
  },

  created(){
    this.getOrders(null)
    this.allPayments(0)
    // console.log( this.customerPayments);
    // this.customerPayments[0].payments.forEach((items) => {
    //     console.log(items);
    // })
    this.$store.state.infoDrawer = false
  },

  methods: {
    getOrders(date){
        let self = this;
        let store = self.$store;
        this.selectedDate = date

        this.$store.dispatch("getReq", {
            url: "order/orders",
            params: {
                date: date,
                // limit: self.$store.state.limit,
                limit: null,
                pagination: self.page,
                user_id: this.$session.get('warehouseId')
                // user_id: this.$session.get('warehouseId') == 0 ? this.$session.get('userId') : this.$session.get('warehouseId')
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

    getPayments(date){
        let self = this;
        let store = self.$store;
        this.selectedDate = date
        this.isAllPayments = false

        this.$store.dispatch("getReq", {
            url: "order/ongoing_payments",
            params: {
                date: date,
                // limit: self.$store.state.limit,
                limit: 0,
                pagination: self.page,
                user_id: this.$session.get('warehouseId'),
                su_id: this.$session.get('userId')
            },
            auth: self.$session.get('token'),
            csrftoken: self.$session.get('token'),
            callback: function(data) {
                // console.log('payments',data);
                store.getters["setData"]([store.state.order.paymentsArr, [data]]);
            },
        });
    },

    paymentDetails(paymentid){
        let self = this;

        this.$store.dispatch('order/getPaymentDetails', {
            url: 'order/payment_details',
            params: {
                customerId: paymentid
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
        this.$store.state.formName = 'Sale';
        this.$store.state.formsTemp = 'OrderStepper';
    },

    displaySearchView(){
        this.searchView = true
    },

    searchOrder(){
        let self = this

        self.searchView = true
        if(this.orderSearch == ''){
            self.searchView = false
            self.$store.state.order.serachOrderArr = []
        }
        // send request
        if(this.orderSearch != ''){
            this.$store.dispatch('getReq', {
                url: 'order/search_order',
                params: {
                    customer_name: self.orderSearch,
                    user_id: self.$session.get('warehouseId')
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data){
                    console.log('search data', data);
                    if(data.founded){
                        self.$store.state.infoTempName = 'PaymentDetails'
                        self.$store.getters["setData"]([self.$store.state.order.serachOrderArr, [data]]);
                    }else{
                        self.$store.state.order.serachOrderArr = []
                    }
                },
            })
    }   
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
        background-color: #ffffff;
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
    .hide-serach-result{
        height: 50px;
        width: 40%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
        cursor: pointer;
    }
    .order-search-form{
        width: 50%;
        height: auto;
        display: flex;
        justify-content: flex-start;
        align-items: flex-end;
    }
    .order-search-form .v-text-field{
         width: 70%;
         margin-right: 20px;
     }
     .order-search-form .v-icon{

     }
    .flex-container{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
    }
    .orders-flex{
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 90%;
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
        margin-bottom: 50px;
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
    .no-payments{
        width: 100%;
        height:90vh;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content:center;
        align-items: center;
    }
    .no-payments .v-icon{
        font-size: 100px;
        color: #1e1d2b;
    }
    .no-payments p{
        text-align: center;
        color: #1e1d2b;
        font-size: 17px;
        font-weight: bold;
    }
    .order-search-result{
        height: 90vh;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .order-founded{
        height: 100%;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .order-no-founded{
        height: 100%;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .pagination-container{
        height: auto;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    @media only screen and (max-width: 500px) {
        .order-core{
            width: 100%;
            align-items: center;
            margin-left: 0%;
        }
        .order-search-form{
            width: 90%;
        }
        .payment-container{
            width: 80%;
        }
        .payment-container .payments p{
            font-size: 12px;
        }
        .pagination-container{
            width: 80%;
        }
        /* .order-core, .orders-flex, .v-tabs, .v-tabs-items{
            margin-left: 20%;
        } */
    }
</style>
