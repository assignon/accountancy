<template>
    <div class='payment-details-core'>
        <div class='details-container'>
            <div class='customer'>
                <h3>Customer Details</h3>
                <p>Name: {{paymentDetails[0].credentials[0].name}}</p>
                <p>Email: {{paymentDetails[0].credentials[0].email}}</p>
                <p v-if='paymentDetails[0].credentials[0].address'>Address: {{paymentDetails[0].credentials[0].address}}</p>
                <p>Tel.number: {{paymentDetails[0].credentials[0].tel_number}}</p>
            </div>
            <div class='payment-details mt-5'>
                <h3>Payment details 
                    <!-- <span style='color:' v-if='paymentDetails[0].payment_helper.completed'>[Payed]</span> -->
                    <!-- <span style='color:magenta' v-else>[Ongoing]</span> -->
                </h3>
                <p>Paying: {{paymentDetails[0].paying}}</p>
                <p>Pay by terms: {{paymentDetails[0].paying_term}}</p>

                <p>Method: {{paymentDetails[0].methods[0].name}}</p>
                <p>Pay in: {{paymentDetails[0].payments[0].pay_in}}</p>
                <p>Payment Interval: {{paymentDetails[0].payments[0].payment_interval}}</p>
                <p>Times: {{paymentDetails[0].customer[0].times}}</p>

                <p>Start Date: {{parseDate(paymentDetails[0].customer[0].start)}}</p>
                <p>End Date: {{parseDate(paymentDetails[0].payment_dates.end)}}</p>
                <p
                    v-if='dateNow < paymentDetails[0].payment_dates.paying_dates[paymentDetails[0].payment_dates.paying_dates.length-1]'
                >
                    Next Payment: {{parseDate(nextPaymentDate(paymentDetails[0].payment_dates.paying_dates))}}
                </p>
                
            </div>
        </div>

        <div class='details-actions'>
            <!-- <v-btn large color='#ce2b58' @click='removePayment()'>
                Delete
                <v-icon style='font-size:15px' class='ml-3' color='#fff'>fas fa-trash-alt</v-icon>
            </v-btn> -->
        </div>
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
            dateNow: new Date().toISOString().split('T')[0]
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

        removePayment(){
            alert()
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
</style>