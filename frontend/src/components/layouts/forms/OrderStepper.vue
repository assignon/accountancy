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
            <small>Summarize if needed</small>
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
            <small>Summarize if needed</small>
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
            <small>Summarize if needed</small>
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
        PaymentForm
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
        addOrder(){
            alert('form filled')
        //     let self = this;
        //     let store = self.$store.state.ls;
        //     let formErrMsg = document.querySelector(".quality-form-err-msg");
        //     let validationErrMsg = document.querySelector('.v-messages__message');
            
        //     if (self.$store.state.ls.qualitycriteriaArr.length >= 3 && store.dod != null) {
        //         if(!document.body.contains(validationErrMsg)){
        //             self.$emit('submit')
        //         }else{
        //             formErrMsg.innerHTML = validationErrMsg.textContent;
        //         }
        //     } else {
        //         formErrMsg.innerHTML = "Definition Of Done field is empty or quality criteria < 7";
        //     }
        },
    },
}
</script>

<style scoped>
    .order-stepper{
      width: 100%;
      height: 94%;
      overflow: hidden;
      margin: auto;
    }
    .v-stepper{
        box-shadow: none;
    }
    .theme--light.v-stepper{
        background-color: #fffafa;
    }
</style>