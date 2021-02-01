<template>
    <div class='pdf-core'>
        <div class='pdf-header'>
            <h2>CHICAM</h2>
            <p style='position:relative;top:10px;'>
                <span class='font-weight-bold'>Date</span><br>
                {{new Date().toDateString()}}
            </p>
        </div>
        <div class='divider'></div>
        <div class='pdf-body'>
            <div class='customer-info-flex'>
                <h3 class='mb-5'>Customer Information</h3>
                <div class='info-format'>
                    <p class='font-weight-bold mb-1'>Name</p>
                    <p class='mb-3'>{{orderDeteails[0].credential[0].name}}</p>
                </div>
                <div class='info-format'>
                    <p class='font-weight-bold mb-1'>Email</p>
                    <p class='mb-3'>{{orderDeteails[0].credential[0].email}}</p>
                </div>
                <div class='info-format' v-if='orderDeteails[0].credential[0].address'>
                    <p class='font-weight-bold mb-1'>Address</p>
                    <p class='mb-3'>{{orderDeteails[0].credential[0].address}}</p>
                </div>
                <div class='info-format'>
                    <p class='font-weight-bold mb-1'>Tel. Number</p>
                    <p class='mb-3'>{{orderDeteails[0].credential[0].tel_number}}</p>
                </div>
            </div>

            <div class='payment-flex'>
                <h3 class='mb-5'>Payments Method</h3>
                <div class='info-format'>
                    <p class='font-weight-bold mb-1'>Start Date</p>
                    <p class='mb-3'>{{orderDeteails[0].customer[0].start}}</p>
                </div>
                <div class='info-format'>
                    <p class='font-weight-bold mb-1'>Pay In</p>
                    <p class='mb-3'>{{orderDeteails[0].payment[0].pay_in}}</p>
                </div>
                <div class='info-format'>
                    <p class='font-weight-bold mb-1'>Payment Interval</p>
                    <p class='mb-3'>{{orderDeteails[0].payment[0].payment_interval}}</p>
                </div>
                <div class='info-format'>
                    <p class='font-weight-bold' mb-1>Method</p>
                    <p class='mb-3'>{{orderDeteails[0].method[0].name}}</p>
                </div>
            </div>
        </div>
        <div class='divider'></div>
        <div class='pdf-footer'>
            <h3 class='mb-5 mt-5'>Orders</h3>
            <div class='info-format'>
                <p class='font-weight-bold'>Order Place on</p>
                <p>{{parseDate(orderDeteails[0].order.order_on)}}</p>
            </div>
            <table class='order-table mt-5'>
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

            <div class='total-price pb-3'>
                <v-btn large color='#1976d2' style='position:relative;top:70px;color:white;text-transform:capitalize;font-weight:bold;' @click='printOrder()'>Print PDF</v-btn>
                <h3>
                    <!-- <span>
                        {{orderDeteails[0].payment_helper.paying_in_terms}} / 
                        {{orderDeteails[0].payment[0].payment_interval}}
                    </span><br> -->
                    <span style='color: #1976d2;'>Total Price: {{orderDeteails[0].paying}}</span>
                </h3>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    name: 'OrderPDF',

    computed: {
        ...mapGetters({
            orderDeteails: 'order/getCustomerOrder',
        }),
    },

    created(){
        console.log('order details', self.orderDeteails);
    },

    methods: {
        printOrder(){
            window.print();
            window.location.reload()
            window.addEventListener('onafterprint', function(){
                window.location.reload()
            }) 
        },

        parseDate(date){
            return new Date(date).toDateString()
        },
    }
}

</script>

<style scoped>
    .pdf-core{
        width: 100%;
        min-height: 100vh;
        height: 100vh;
        overflow-y: scroll;
        overflow-x: hidden;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        background-color: red;
    }
    ::-webkit-scrollbar {
         width: 10px;
    }
    .pdf-header{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 50px;
    }
    .pdf-body{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        margin-top: 50px;
        margin-bottom: 50px;
    }
    .customer-info-flex, .payment-flex{
        width: 50%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .info-format{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .pdf-core h2, .pdf-core h2{
        color: #1976d2;
        text-align: left;
    }
    .pdf-core h3{
        color: #15141c;
    }
    .pdf-core p{
        color: #15141c;
        font-size:15px;
        text-align: left;
        margin: 0px;
        padding: 0px;
    }
    .pdf-footer{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .order-table{
        width: 80%;
    }
    .order-table, th, td {
        border: 1px solid #1e1d2b;
        border-collapse: collapse;
        color: #1e1d2b;
        padding: 5px 20px 5px 20px;
        font-size: 17px;
        text-align: left;
    }
    .order-table, td p{
        color: #1e1d2b;
    }
    .total-price{
        width: 80%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-end;
        margin-top: 10px;
    }
    .divider{
        width: 100%;
        border: 0.5px solid #1e1d2b;
    }
</style>