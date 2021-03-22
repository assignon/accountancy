<template>
    <div class='payment-details-core'>
        <div class='details-container'>
            <div class='customer'>
                <h3>Customer Details</h3>
                <p>Name: {{paymentDetails[0].credentials[0].name}}</p>
                <p v-if='paymentDetails[0].credentials[0].email'>Email: {{paymentDetails[0].credentials[0].email}}</p>
                <p v-else>Email: None</p>
                <p v-if='paymentDetails[0].credentials[0].address'>Address: {{paymentDetails[0].credentials[0].address}}</p>
                <p>Tel.number: {{paymentDetails[0].credentials[0].tel_number}}</p>
            </div>
            <div class='payment-details mt-5'>
                <h3>Payment details 
                    <!-- <span style='color:' v-if='paymentDetails[0].payment_helper.completed'>[Payed]</span> -->
                    <!-- <span style='color:magenta' v-else>[Ongoing]</span> -->
                </h3>
                <p>Paying: {{formatPrice(paymentDetails[0].paying)}}FRS</p>
                <p>Pay by terms: {{formatPrice(paymentDetails[0].paying_term)}}FRS</p>

                <p>Method: {{paymentDetails[0].methods[0].name}}</p>
                <p>Pay in: {{paymentDetails[0].payments[0].pay_in}}</p>
                <p>Payment Interval: {{paymentDetails[0].payments[0].payment_interval}}</p>
                <p>Times: {{paymentDetails[0].customer[0].times}}</p>

                <p>Start Date: {{parseDate(paymentDetails[0].customer[0].start)}}</p>
                <p>End Date: {{parseDate(paymentDetails[0].payment_dates.end)}}</p>
                <p
                    v-if='currentDate < paymentDetails[0].payment_dates.paying_dates[paymentDetails[0].payment_dates.paying_dates.length-1]'
                >
                    Next Payment: {{parseDate(nextPaymentDate(paymentDetails[0].payment_dates.paying_dates))}}
                </p> 
                <div class='payment-status-core'> 
                    <h3>Payment Status</h3>
                    <div class='payment-status-container' v-for='(ps, i) in paymentDetails[0].p_status' :key='i'>
                        <p>{{ps.payment_date}}</p>
                        <div class='check-bc ml-5'>
                            <v-checkbox
                                v-model="ps.payed"
                                v-if='$session.get("su")'
                                :value="ps.payed"
                                label=""
                                class=''
                                style='position:relative;bottom:20px;'
                                @click='displayConfirmationDialog(ps.payed, paymentDetails[0].customer[0].id, ps.payment_date,paymentDetails[0].customer[0].order_id, paymentDetails[0].paying_term), $store.state.order.updateCustomPrice=false'
                            ></v-checkbox>
                        </div>
                        <p class='ml-3'>{{ps.employee_name}}</p>
                        <div class='remaining-payment ml-5' v-if="ps.custome_payment>0 && paymentDetails[0].paying_term>ps.custome_payment">
                            <p>Remain ({{formatPrice(paymentDetails[0].paying_term-ps.custome_payment)}}FRS)</p>
                            <v-btn 
                                medium color='#0163d1'
                                class='ml-3'
                                @click='displayConfirmationDialog(ps.payed, paymentDetails[0].customer[0].id, ps.payment_date,paymentDetails[0].customer[0].order_id, paymentDetails[0].paying_term), employeeName=ps.employee_name, $store.state.order.updateCustomPrice=true'
                            >
                                <span style='color:white'>Complete</span>
                            </v-btn>
                        </div>
                    </div>
                </div>
                
            </div>
        </div>

        <div class='details-actions'>
            <!-- <v-btn large color='#ce2b58' @click='removePayment()'>
                Delete
                <v-icon style='font-size:15px' class='ml-3' color='#fff'>fas fa-trash-alt</v-icon>
            </v-btn> -->
        </div>
        <v-dialog
            v-model="paymentConfirmationDialog"
            persistent
            max-width="600px"
        >
            <div class='payment-confirmation-container'>
                <p class='confirmation-text' style='font-size: 17px;font-weight:bold;text-align:left;'></p>
                <!-- <span style='font-size: 17px;text-align:left;' class='mb-3 err-msg'></span> -->
                <v-text-field
                    v-model="employeeName"
                    :rules="[$store.state.rules.required]"
                    label="Employee Name*"
                    required
                    outlined
                    style='width:90%;'
                ></v-text-field>
                <v-text-field
                    v-model="customePayment"
                    label="Custom Price"
                    outlined
                    type='number'
                    style='width:90%;'
                ></v-text-field>
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
import { mapGetters } from 'vuex';
export default {
    name: 'PaymentDetails',

    computed: {
        ...mapGetters({
            paymentDetails: 'order/getcustomerPayment',
        }),
    },

    data(){
        return {
            currentDate: new Date().toISOString().split('T')[0],
            // current_status: null, //payment status of the current date
            paymentConfirmationDialog: false,
            paymentStatus: null, 
            customerID: null,
            updatedPaymentdate: null,
            employeeName: null,
            orderId: null,
            customePayment: 0,
            payByTerms: null,
        }
    },

    created() {
    },

    methods: {
         parseDate(date){
            return new Date(date).toDateString()
        },

        nextPaymentDate: function(dates_arr){
            let currentDate = new Date().toISOString().split('T')[0]
            let dateIndexArr = []

            dates_arr.forEach(date => {
                if (currentDate >= date){
                    dateIndexArr = []
                    dateIndexArr.push(dates_arr.indexOf(date))
                }
            })
            return dates_arr[dateIndexArr[0]+1]
        },

        formatPrice(value) {
            let val = (value/1).toFixed(0).replace('.', ',')
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
        },

        removePayment(){
            alert()
        },

        displayConfirmationDialog(updateValue, customerId, updatedPaymentdate,orderId, pay_terms){
            let self = this;
            self.paymentConfirmationDialog = true
            // document.querySelector('.err-msg').innerHTML = 'Update Custom price'
            setTimeout(() => {
                self.paymentStatus = updateValue
                self.customerID = customerId
                self.orderId= orderId
                self.updatedPaymentdate = updatedPaymentdate
                self.payByTerms = pay_terms
                if(!self.$store.state.order.updateCustomPrice){
                    document.querySelector('.confirmation-text').innerHTML = updateValue ? 
                    'Current payment status: NOT PAYED <br> Do you wanna update the current paymentstatus?' :
                    'Current payment status: PAYED <br> Do you wanna update the current payment status?'
                }else{
                     document.querySelector('.confirmation-text').innerHTML = 'Update Custom price'
                }
            }, 100)
        },

        cancelPaymentUpdate(){
            self.paymentConfirmationDialog=false
            window.location.reload()
        },

        updatePaymentStatus(){
            let self = this;
            let validationErrMsg = document.querySelector('.v-messages__message');
            let body = {
                new_value: self.paymentStatus,
                customer_id: self.customerID,
                payment_date: self.updatedPaymentdate,
                employee_name: self.employeeName,
                order_id: self.orderId,
                custome_payment: self.customePayment,
                update_custom_price: self.$store.state.order.updateCustomPrice,
            }
            if(this.employeeName != null && !document.body.contains(validationErrMsg)){
                if(self.payByTerms >= self.customePayment){
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
                }else if(self.payByTerms < self.customePayment){
                    alert(`The order total price (${self.payByTerms}) cannot be less than the custom price`)
                }
            }
        }
    }
}
</script>

<style scoped>
    .payment-details-core{
        height: 90vh;
        width: 95%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        margin-top: 15px;
        margin-left: 70px;
    }
    .details-container{
        height: 90%;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .customer, .payment-details{
        height: auto;
        width: 500px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .customer h3, .payment-details h3{
        color: white;
        margin-bottom: 10px;
    }
    .customer p, .payment-details p{
        color: white;
        text-align: 15px;
        padding: 0px;
        margin: 0px;
        margin-bottom: 10px;
    }
    .payment-dates{
        height: auto;
        width: auto;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .payment-dates .dates{
        height: auto;
        width: auto;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }
    .payment-status-core{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .payment-status-container{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .check-bc{
        width: 22px;
        height: 22px;
        background-color: white;
    }
    .remaining-payment{
        width: auto;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }
    .details-actions{
        height: 10%;
        width: 90%;
        display: flex;
        justify-content: flex-end;
        align-items: flex-end;
    }
    .details-actions .v-btn{
        text-transform: capitalize;
        color: white;
        font-weight: bold;
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