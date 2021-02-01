<template>
    <v-stepper
        v-model="orderFormStep"
        vertical
        class='order-stepper pt-5'
        style='padding-left: 70px'
    >   <!-- customer information -->
        <v-stepper-step
            :complete="orderFormStep > 1"
            step="1"
        >
            Customer Informtions
            <!-- <small>Summarize if needed</small> -->
        </v-stepper-step>

        <v-stepper-content step="1">
            <CustomerInformationsForm :orderstep="orderFormStep" @updatestep='orderFormStep = 2' />
        </v-stepper-content>
        <!-- order -->
        <v-stepper-step
            :complete="orderFormStep > 2"
            step="2"
        >
            Order
            <!-- <small>Summarize if needed</small> -->
        </v-stepper-step>

        <v-stepper-content step="2">
            <OrderForm :orderstep="orderFormStep" @updateprevstep='orderFormStep = 1' @updatestep='orderFormStep = 3' />
        </v-stepper-content>
        <!-- payment details -->
        <v-stepper-step
            :complete="orderFormStep > 3"
            step="3"
        >
            Payment Informtions
            <!-- <small>Summarize if needed</small> -->
        </v-stepper-step>

        <v-stepper-content step="3">
            <PaymentForm :orderFormStep="orderFormStep" @updateprevstep='orderFormStep = 2' @submit='addOrder()' />
        </v-stepper-content>
    </v-stepper>
</template>

<script>
import OrderForm from "@/components/layouts/forms/OrderForm.vue";
import CustomerInformationsForm from "@/components/layouts/forms/CustomerInformationsForm.vue";
import PaymentForm from "@/components/layouts/forms/PaymentForm.vue";
export default {
    name: 'OrderFormStep',
    
    props: [],

    components: {
        OrderForm,
        CustomerInformationsForm,
        PaymentForm,
    },

    computed: {
    },

    data(){
        return{
            orderFormStep: 1
        }
    },
    created(){},

    methods: {
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

        addOrder(){
            let self = this;
            let store = self.$store.state.order;
            // let formErrMsg = document.querySelector(".payment-form-err-msg");
            let body = {
                // customer informations
                email: store.email,
                name: store.name,
                address: store.address,
                tel_number: store.telNumber,
                times: store.times,
                start: store.startDate,
                // order informations
                ordered_products: store.productArr,
                // payment informations
                payment_interval: store.payInterval,
                pay_in: store.payIn,
                method: store.payMethod,
            }

            this.$store.dispatch("postReq", {
                url: "order/new_order",
                params: body,
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log('added',data);
                    if(data.created){
                        // window.location.reload();
                        self.customerOrder(data.order_id)
                        self.$store.state.pdfTemp = 'OrderPdf';
                        self.$store.state.pdfDialog = true;
                    }
                },
            });
        },
    }
}
</script>

<style scoped>
    .order-stepper{
      width: 100%;
      height: auto;
      min-height: 94%;
      overflow-y: scroll;
      overflow-x: hidden;
      margin: auto;
      padding-bottom: 10px;
    }
    .v-stepper{
        box-shadow: none;
    }
    .theme--light.v-stepper{
        background-color: #fffafa;
    }
</style>