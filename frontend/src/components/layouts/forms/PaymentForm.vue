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
            :menu-props="{ bottom: true, offsetY: true }"
            label="Pay in*"
            outlined
        ></v-select>
        <div v-if='$store.state.order.payIn == "Terms"' class='pay-interval-times'>
            <v-flex xs12 sm12 md8 lg8 xl8>
                <v-select
                    v-model="$store.state.order.payInterval"
                    :rules="[$store.state.rules.required]"
                    :items="selectPayIntervalArr"
                    :menu-props="{ bottom: true, offsetY: true }"
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
        <div class='payment-method-field-container'>
            <v-select
                v-model="$store.state.order.payMethod"
                :rules="[$store.state.rules.required]"
                :items="selectPayMethodArr"
                :menu-props="{ bottom: true, offsetY: true }"
                label="Payment Method*"
                outlined
            ></v-select>
            <v-icon 
                style='font-size:50px;' 
                color='#0163d1' 
                @click='extraItemDialog = true'
                class='ml-5'
            >fas fa-plus-square</v-icon>
        </div>
        
        <div class="btn-container">
          <v-btn
                depressed
                height="50"
                :width="btnWidth"
                class="fot-weight-bold white--text mr-2"
                color="#1976d2"
                @click="updatePreviousStep(orderStep)"
          >
            <p style='font-size:17px;margin:auto;'>Previous</p>
          </v-btn>

          <v-btn
            depressed
            height="50"
            :width="btnWidth"
            class="fot-weight-bold white--text"
            color="#1976d2"
            @click="submitOrder(orderStep)"
          >
            <p style='font-size:17px;margin:auto;'>Add Order</p>
          </v-btn>
        </div>
         <!-- add extra item dialog -->
        <v-dialog
            v-model="extraItemDialog"
            persistent
            max-width="600px"
        >
            <v-form class='new-extra'>
                <p class="headline mb-4">Add New Payment Method</p>
                <v-spacer></v-spacer>
                <p class='new-extra-err mb-4'></p>
                <v-text-field
                    :label='Name'
                    required
                    outlined
                    :rules="[$store.state.rules.required]"
                    v-model='extraItemName'
                ></v-text-field>
                <v-spacer></v-spacer>
                <div class='btn-container'>
                    <v-btn
                        color="blue darken-1"
                        text
                        @click="extraItemDialog = false"
                    >
                        Close
                    </v-btn>
                    <v-btn
                    depressed
                        height="50"
                        :width="btnWidth"
                        class="fot-weight-bold white--text"
                        color="#1976d2"
                        @click="addNewMethod()"
                    >
                        <p style='font-size:17px;margin:auto;'>Add</p>
                    </v-btn>
                </div>
            </v-form>
        </v-dialog>
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
            extraItemName: null,
            extraItemDialog: false,
            btnWidth: window.innerWidth > 500 ? '20%' : '45%',
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
                        self.selectPayMethodArr.push(self.capitalizeFirstLetter(item.method))
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

        capitalizeFirstLetter(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        },

        addNewMethod(){
            // add extra profile, brand or vehicle
            let self = this;
            // let store = self.$store;
            
            let formErrMsg = document.querySelector(".new-extra-err");
            // let validationErrMsg = document.querySelector('.v-messages__message');

            if(self.extraItemName != null){
                let body = {
                    name: self.capitalizeFirstLetter(self.extraItemName)
                }

                if(self.selectPayMethodArr.includes(self.capitalizeFirstLetter(self.extraItemName))){
                    formErrMsg.innerHTML = `This payment method already exists`;
                    return false
                }

                self.$store.dispatch("postReq", {
                    url: "payment/new_payment_method",
                    params: body,
                    auth: self.$session.get('token'),
                    csrftoken: self.$session.get('token'),
                    callback: function(data) {
                        if(data.added){
                            // add new extra to array
                            self.selectPayMethodArr.push(self.capitalizeFirstLetter(self.extraItemName))
                            formErrMsg.innerHTML = data.msg
                            document.querySelector('.new-extra').reset()
                            //close dialog after 2sec
                            setTimeout(() => {
                                self.extraItemDialog = false
                                formErrMsg.innerHTML = ''
                            }, 2000)
                        }else{
                            formErrMsg.innerHTML = data.msg
                        }
                    },
                });
            }else{
                formErrMsg.innerHTML = `Give the name of the payment method`;
            }
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
    .payment-method-field-container{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .new-extra{
        width: 100%;
        height: auto;
        padding: 30px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        background-color: white;
    }
    .new-extra .v-text-field{
         width: 100%;
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
    @media only screen and (max-width: 500px){
        .payment-form{
             width: 100%;
         }
        .products-fields, .brands-profiles-select{
            flex-direction: column;
            justify-content: flex-start;
        }
        .products-fields, .brands-profiles-select{
            width: 100%;
            flex-direction: column;
            justify-content: flex-start;
        }
        .btn-container{
            width: 100%;
        }
        .add-product{
            margin-bottom: 20px;
        }
    }
</style>