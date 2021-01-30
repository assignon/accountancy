<template>
    <div class='order-details-core'>
        <div class='details-container'>
            <div class='customer'>
                <h3>Customer Details</h3>
                <p>Name: {{orderDeteails[0].credential[0].name}}</p>
                <p>Email: {{orderDeteails[0].credential[0].email}}</p>
                <p v-if='orderDeteails[0].credential[0].address'>Address: {{orderDeteails[0].credential[0].address}}</p>
                <p>Tel.number{{orderDeteails[0].credential[0].tel_number}}</p>
            </div>

            <div class='order-details mt-5'>
                <h3>Order Details</h3>
                <p>Order on: {{parseDate(orderDeteails[0].order.order_on)}}</p>
                <table class='order-table'>
                    <tr>
                        <th>Size</th>
                        <th>Brands</th>
                        <th>Vehical</th>
                        <th>Profiles</th>
                        <th>Price</th>
                        <th>Quantity</th>
                    </tr>
                    <tr v-for="(product,i) in orderDeteails[0].products" :key="i" >
                        <td>{{product.products[0].size}}</td>
                        <td>
                            <p v-for="(brand, b) in product.brands" :key="b">{{brand.name}}</p>
                        </td>
                        <td>{{product.vehicule[0].name}}</td>
                        <td>
                            <p v-for="(profile, p) in product.profiles" :key="p">{{profile.name}}</p>
                        </td>
                        <td>{{product.products[0].price}}</td>
                        <td>{{product.ordered_product.quantity}}</td>
                    </tr>
                </table>
            </div>

            <div class='payment-details mt-5'>
                <h3>Payment details 
                    <span style='color:' v-if='orderDeteails[0].payment_helper.completed'>[Payed]</span>
                    <span style='color:magenta' v-else>[Ongoing]</span>
                </h3>
                <p>Paying: {{orderDeteails[0].paying}}</p>
                <p>Method: {{orderDeteails[0].method[0].name}}</p>
                <p>Pay by terms: {{orderDeteails[0].payment_helper.paying_in_terms}}</p>
                <p>Pay in: {{orderDeteails[0].payment[0].pay_in}}</p>
                <p>Payment Interval: {{orderDeteails[0].payment[0].payment_interval}}</p>
                <p>Start Date: {{orderDeteails[0].customer[0].start}}</p>
                <p>Times: {{orderDeteails[0].customer[0].times}}</p>
                <div class='payment-dates'>
                    <p>Payment Dates:</p>
                    <div class='dates ml-2' 
                        v-for='(dates, pd) in orderDeteails[0].payment_helper.paymentDates_end.paying_dates' 
                        :key="pd"
                    >
                        <p>{{dates}} ,</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- <div class='details-actions'>
            <v-btn large color='#ce2b58' @click='removeOrder()'>
                Delete
                <v-icon style='font-size:15px' class='ml-3' color='#fff'>fas fa-trash-alt</v-icon>
            </v-btn>
        </div> -->
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    name: 'OrderDetails',

    computed: {
        ...mapGetters({
            orderDeteails: 'order/getCustomerOrder',
        }),
    },

    data(){
        return {
      
        }
    },

    created() {
    },

    methods: {
         parseDate(date){
            return new Date(date).toDateString()
        },

        removeOrder(){

        }
    }
}
</script>

<style scoped>
    .order-details-core{
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
        overflow-y: scroll;
        overflow-x: hidden;
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
     .details-actions{
        height: 10%;
        width: 80%;
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