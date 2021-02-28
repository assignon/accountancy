<template>
    <div class='order-temp-core'>
        <v-layout 
            class='order-temp-layout animated fadeInUp'
            v-for="(order,i) in orderArr[0].order"
            :key='i'
            :style="[oder_totaly_paid(order.p_status).includes(false) ? {borderLeft:'7px solid red'} : {borderLeft:'7px solid green'}]" 
        >
            <v-flex xs12 sm12 md2 lg2 xl2 class='customer-name' @click.stop='$store.state.infoDrawer=true, customerOrder(order.customer_id)'>
                <v-icon medium color='#1e1d2b'>fas fa-user-circle</v-icon>
                <p>{{order.credentials.name}}</p>
            </v-flex>

            <v-flex xs12 sm12 md3 lg3 xl3 class='product-name' @click.stop='$store.state.infoDrawer=true, customerOrder(order.customer_id)'>
                <p>
                    <v-icon small color='#1e1d2b' class='mr-1'>fas fa-boxes</v-icon>
                    {{order.ordered_products[0].product[0].size}} 
                    <span>( {{order.ordered_products[0].ordered_product.quantity}}x )</span>
                    <span class='ml-2' v-if='order.ordered_products.length>=2'>[ +{{order.ordered_products.length-1}} ]</span></p>
            </v-flex>

            <v-flex xs12 sm12 md4 lg3 xl3 class='date' @click.stop='$store.state.infoDrawer=true, customerOrder(order.customer_id)'>
                <p>
                    <v-icon small color='#1e1d2b' class='mr-1'>fas fa-calendar-alt</v-icon>
                    {{parseDate(order.order.order_on)}}
                </p>
            </v-flex>

            <v-flex xs12 sm12 md3 lg3 xl3 class='price' @click.stop='$store.state.infoDrawer=true, customerOrder(order.customer_id)'>
                <p>
                    <v-icon small color='#1e1d2b' class='mr-1'>fas fa-coins</v-icon>
                    {{formatPrice(order.paying)}}FRS
                </p>
            </v-flex>

            <!-- <v-flex xs12 sm12 md3 lg3 xl3 class='payment-method nav-layout hidden-md-and-down'>
                <p>
                    <v-icon small color='#1e1d2b' class='mr-1'>fas fa-credit-card</v-icon>
                    {{order.payment.method[0].name}}
                </p>
            </v-flex> -->
            <div  v-if='order.payment.pay_in != "Once"'>
                <v-flex xs12 sm12 md2 lg2 xl2 
                    :style="[currentDate == ps.payment_date ? {display:'flex'} : {display:'none'}]" 
                    :class='currentDate' 
                    v-for='(ps, i) in order.p_status' 
                    :key='i'
                > <!-- ther could be multiple payment dates -->
                    <v-checkbox
                        v-if='currentDate == ps.payment_date'
                        v-model="ps.payed"
                        :value="ps.payed"
                        label="PAID"
                        @click='displayConfirmationDialog(ps.payed, order.customer_id, ps.payment_date)'
                    ></v-checkbox>
                </v-flex>
            </div>
    
            <v-flex xs12 sm12 md2 lg2 xl2 
                v-else
                :class='currentDate' 
            > 
                <v-checkbox
                    v-model="order.p_status[0].payed"
                    :value="order.p_status[0].payed"
                    label="PAID"
                    @click='displayConfirmationDialog(order.p_status[0].payed, order.customer_id, order.p_status[0].payment_date)'
                ></v-checkbox>
            </v-flex>

        </v-layout>
        <v-dialog
            v-model="paymentConfirmationDialog"
            persistent
            max-width="600px"
        >
            <div class='payment-confirmation-container'>
                <p class='confirmation-text' style='font-size: 17px;font-weight:bold;text-align:left;'></p>
                <div class="btn-container">
                <v-btn
                    depressed
                    height="50"
                    width="20%"
                    class="fot-weight-bold white--text mr-2"
                    color="#1976d2"
                    @click="cancelPaymentUpdate"
                >
                    <p style='font-size:17px;margin:auto;'>No</p>
                </v-btn>

                <v-btn
                    depressed
                    height="50"
                    width="20%"
                    class="fot-weight-bold white--text"
                    color="#1976d2"
                    @click="updatePaymentStatus"
                >
                    <p style='font-size:17px;margin:auto;'>Yes</p>
                </v-btn>
                </div>
            </div>
        </v-dialog>
    </div>
</template>

<script>
// import Vue from 'vue';
// Vue.forceUpdate();
export default {
    name: 'OrderTemp',

    props:['orderArr'],

    computed: {
    },

    data(){
        return{
            currentDate: new Date().toISOString().split('T')[0],
            // current_status: null, //payment status of the current date
            paymentConfirmationDialog: false,
            paymentStatus: null, 
            customerID: null,
            updatedPaymentdate: null,
        }
    },

    created(){
        // console.log(this.orderArr[0].order);
        console.log(this.orderArr[0]);
    },

    methods: {
        forceRerender() {
            // Remove my-component from the DOM
            this.renderComponent = false;

            this.$nextTick(() => {
            // Add the component back in
                this.renderComponent = true;
            });
        },

        oder_totaly_paid(pStatus){
            let statusArr = [];
            
            pStatus.forEach((item) => {
                if(item.payed == true){
                    statusArr.push(true)
                }else{
                    statusArr.push(false)
                }
            })
            return statusArr
        },

        parseDate(date){
            return new Date(date).toDateString()
        },

        formatPrice(value) {
            let val = (value/1).toFixed(0).replace('.', ',')
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
        },

        getPaymentStatus(paymentStatusArr){
            let self = this
            let currentDate = new Date().toISOString().split('T')[0]
            let status = null

            paymentStatusArr.forEach(ps => { // ps=payment status
                if(currentDate == ps.payment_date){
                    status = {payed: ps.payed, text: ps.payed ? 'Payed' : 'Not Yet'}
                }
            })
            self.$store.state.order.currentStatus = status
            return status
        },

        customerOrder(customerID){
            let self = this;
            this.$store.dispatch('order/getOrderDetails', {
                url: 'order/order_details',
                params: {
                    customerId: customerID
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data){
                    // console.log('api data', data);
                    self.$store.state.infoTempName = 'OrderDetails'
                    self.$store.getters["setData"]([self.$store.state.order.customerOrderArr, [data]]);
                    
                },
            })
        },

        displayConfirmationDialog(updateValue, customerId, updatedPaymentdate){
            let self = this;
            self.paymentConfirmationDialog = true
            setTimeout(() => {
                self.paymentStatus = updateValue
                self.customerID = customerId
                self.updatedPaymentdate = updatedPaymentdate
                document.querySelector('.confirmation-text').innerHTML = updateValue ? 
                'Current payment status: NOT PAID <br> Do you wanna update the current paymentstatus?' :
                'Current payment status: PAID <br> Do you wanna update the current payment status?'
            }, 100)
        },

        cancelPaymentUpdate(){
            self.paymentConfirmationDialog=false
            window.location.reload()
        },

        updatePaymentStatus(){
            let self = this;
            let body = {
                new_value: self.paymentStatus,
                customer_id: self.customerID,
                payment_date: self.updatedPaymentdate
            }

            this.$store.dispatch("putReq", {
                url: "payment/update_payment_status",
                params: body,
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    console.log(data);
                    if(data.updated){
                       document.querySelector('.confirmation-text').innerHTML = data.msg
                       setTimeout(() => {
                           self.paymentConfirmationDialog = false
                       }, 1500)
                    }
                },
            });
        }
    }
}
</script>

<style scoped>
    .order-temp-core{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-top: 15px;
    }
    .order-temp-layout{
        height: auto;
        width: 95%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
        border: 1px solid #ebf0f7;
        border-radius: 10px;
        background-color: #ebf0f7;
        padding: 5px;
        cursor: pointer;
        margin-bottom: 20px;
        box-shadow: rgba(255, 255, 255, 0.2) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0.9) 0px 0px 0px 1px;
    }
    .customer-name{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .date p, .customer-name p, .product-name p, .price p, .payment-method p{
        color: #1e1d2b;
        font-size: 15px;
        text-align: center;
        width: 100%;
        padding: 0px;
        margin: 0px;
        font-weight: bold;
        overflow: hidden;
    }
    .payment-confirmation-container{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: #fffafa;
        padding: 50px;
    }
    .btn-container{
        width: 100%;
        height: auto;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    .v-btn{
        text-transform: capitalize;
    }
   
</style>