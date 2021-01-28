<template>
    <div class='payment-details-core'>
        <div class='customer'>
            <h3>Customer Details</h3>
            <p>Name: {{paymentDeteails[0].credentials[0].name}}</p>
            <p>Email: {{paymentDeteails[0].credentials[0].email}}</p>
            <p v-if='paymentDeteails[0].credentials[0].address'>Address: {{paymentDeteails[0].credentials[0].address}}</p>
            <p>Tel.number: {{paymentDeteails[0].credentials[0].tel_number}}</p>
        </div>
        <div class='payment-details mt-5'>
            <h3>Payment details 
                <!-- <span style='color:' v-if='paymentDeteails[0].payment_helper.completed'>[Payed]</span> -->
                <!-- <span style='color:magenta' v-else>[Ongoing]</span> -->
            </h3>
            <p>Paying: {{paymentDeteails[0].paying}}</p>
            <p>Pay by terms: {{paymentDeteails[0].paying_term}}</p>

            <p>Method: {{paymentDeteails[0].methods[0].name}}</p>
            <p>Pay in: {{paymentDeteails[0].payments[0].pay_in}}</p>
            <p>Payment Interval: {{paymentDeteails[0].payments[0].payment_interval}}</p>
            <p>Times: {{paymentDeteails[0].payments[0].times}}</p>

            <p>Start Date: {{parseDate(paymentDeteails[0].payments[0].start)}}</p>
            <p>End Date: {{parseDate(paymentDeteails[0].payment_dates.end)}}</p>
            <p
                v-if='dateNow < paymentDeteails[0].payment_dates.paying_dates[paymentDeteails[0].payment_dates.paying_dates.length-1]'
            >
                Next Payment: {{parseDate(nextPaymentDate(paymentDeteails[0].payment_dates.paying_dates))}}
            </p>
            
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    name: 'PaymentDetails',

    computed: {
        ...mapGetters({
            paymentDeteails: 'order/getcustomerPayment',
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
                if (currentDate > date){
                    dateIndexArr = []
                    dateIndexArr.push(dates_arr.indexOf(date))
                }
            })

            return dates_arr[dateIndexArr[0]+1]
        }
    }
}
</script>

<style scoped>
    .payment-details-core{
        height: auto;
        width: 95%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        margin-top: 15px;
        margin-left: 70px;
    }
    .customer, .order-details, .payment-details{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .customer h3, .payment-details h3, .order-details h3{
        color: white;
        margin-bottom: 10px;
    }
    .customer p, .payment-details p, .order-details p{
        color: white;
        text-align: 15px;
        padding: 0px;
        margin: 0px;
        margin-bottom: 10px;
    }
    .order-table{
        width: 80%;
    }
    .order-table, th, td {
        border: 1px solid #1e1d2b;
        border-collapse: collapse;
        color: white;
        padding: 5px 20px 5px 20px;
        font-size: 15px;
        text-align: left;
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
</style>