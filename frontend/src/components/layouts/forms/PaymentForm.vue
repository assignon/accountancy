<template>
    <v-form class="payment-form animated" ref="paymentForm">
        <p class='payment-form-err-msg mb-5'></p>
        
         <v-menu
            v-model="menuStart"
            :close-on-content-click="false"
            :nudge-right="40"
            transition="scale-transition"
            offset-y
            min-width="290px"
            class='start-date'
        >
            <template v-slot:activator="{ on, attrs }">
                <v-text-field
                    v-model="$store.state.order.startDate"
                    label="Start"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    required
                    outlined
                ></v-text-field>
            </template>
            <v-date-picker
                v-model="$store.state.order.startDate"
                @input="menuStart = false"
                :allowed-dates="allowedDates"
            ></v-date-picker>
        </v-menu>
        <v-select
            v-model="$store.state.order.payIn"
            :rules="[$store.state.rules.required]"
            :items="selectPayInArr"
            label="Pay in*"
            outlined
        ></v-select>
        <div v-if='$store.state.order.payIn == "Terms"' class='pay-interval-times'>
            <v-flex xs12 sm12 md8 lg8 xl8>
                <v-select
                    v-model="$store.state.order.payInterval"
                    :rules="[$store.state.rules.required]"
                    :items="selectPayIntervalArr"
                    label="Payment Interval*"
                    outlined
                ></v-select>
            </v-flex>
            <v-flex xs12 sm12 md3 lg3 xl3>
                <v-text-field
                    v-model="$store.state.order.times"
                    :rules="[$store.state.rules.required]"
                    label="Times*"
                    type="number"
                    required
                    outlined
                ></v-text-field>
            </v-flex>
        </div>
        <v-select
            v-model="$store.state.order.payMethod"
            :rules="[$store.state.rules.required]"
            :items="selectPayMethodArr"
            label="Payment Method*"
            outlined
        ></v-select>
        
        <div class="btn-container">
          <v-btn
                depressed
                height="50"
                width="20%"
                class="fot-weight-bold white--text mr-2"
                color="#1976d2"
                @click="updatePreviousStep(orderStep)"
          >
            <p style='font-size:17px;margin:auto;'>Previous</p>
          </v-btn>

          <v-btn
            depressed
            height="50"
            width="20%"
            class="fot-weight-bold white--text"
            color="#1976d2"
            @click="submitOrder(orderStep)"
          >
            <p style='font-size:17px;margin:auto;'>Add Order</p>
          </v-btn>
        </div>
    </v-form>
</template>

<script>
import { mapGetters } from "vuex";
export default {
    name: 'OrderForm',

    props: ["orderStep"],

    computed: {
        ...mapGetters({
            products: 'product/getProducts',
            paymentMethods: 'product/getPaymentMethods',
        }),
       
    },
    data(){
        return{
            menuStart: false,
            selectPayInArr: ['Terms', 'Once'],
            selectPayMethodArr: [],
            selectPayIntervalArr: ['Daily', 'Weekly', 'Monthly'],
        }
    },
    created(){
        this.allProducts()
        this.getPaymentMethods()
    },

    methods: {
        // allowedDates: val => parseInt(val.split('-')[2], 10) % 2 === 0,
        allowedDates: val => val >= new Date().toISOString(),

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
                    data.tire.forEach(item => {
                        self.selectItemsArr.push(item.size)
                    })
                    store.getters["setData"]([store.state.product.productsArr, [data]]);
                },
            });
        },

        getPaymentMethods(){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "payment/payment_methods",
                params: {
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    data.forEach(item => {
                        self.selectPayMethodArr.push(item.method)
                    })
                    console.log(data);
                    store.getters["setData"]([store.state.order.paymentMethodsArr, [data]]);
                },
            });
        },

        submitOrder(stepNum){
            let self = this;
            let store = self.$store.state.order;
            let formErrMsg = document.querySelector(".payment-form-err-msg");
            let validationErrMsg = document.querySelector('.v-messages__message');
            if (store.payIn != null && store.payMethod != null) {
                // if(new Date().toISOString() <= store.startDate){
                    if(store.payIn == 'Once'){
                        if(!document.body.contains(validationErrMsg)){
                            this.$emit('submit', stepNum)
                        }else{
                            formErrMsg.innerHTML = validationErrMsg.textContent;
                        }
                    }else{
                        if(store.payInterval != null && store.times > 0){
                            if(!document.body.contains(validationErrMsg)){
                                this.$emit('submit', stepNum)
                            }else{
                                formErrMsg.innerHTML = validationErrMsg.textContent;
                            }
                        }else{
                            formErrMsg.innerHTML = "Times and pay interval should not be empty"
                        }
                    }
                // }else{
                //     formErrMsg.innerHTML = "The start date cannot be in the past"
                // }
            } else {
                formErrMsg.innerHTML = "Fields are empty";
            }
        },

        updatePreviousStep(stepNum){
            this.$emit('updateprevstep', stepNum)
        },
    },
}
</script>

<style scoped>
    .payment-form{
        width: 70%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
    .payment-form .v-text-field{
         width: 100%;
     }
    .payment-form-err-msg{
        width: 100%;
        height: auto;
        text-align: left;
        color: #15141c;
        font-size: 15px;
    }
    .pay-interval-times{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        /* margin-bottom: 20px;
        margin-top: 20px; */
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