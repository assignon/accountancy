<template>
    <div class='order-temp-core'>
        <v-layout 
            class='order-temp-layout animated fadeInUp'
            v-for="(order,i) in orderArr[0].order"
            :key='i'
            @click.stop='$store.state.infoDrawer=true, customerOrder(order.credentials.customer_id)'
        >
            <v-flex xs12 sm12 md2 lg2 xl2 class='customer-name'>
                <v-icon medium color='#1e1d2b'>fas fa-user-circle</v-icon>
                <p>{{order.credentials.name}}</p>
            </v-flex>

            <v-flex xs12 sm12 md3 lg3 xl3 class='product-name'>
                <p>
                    <v-icon small color='#1e1d2b' class='mr-1'>fas fa-boxes</v-icon>
                    {{order.ordered_products[0].product[0].size}} 
                    <span>( {{order.ordered_products[0].ordered_product.quantity}}x )</span>
                    <span class='ml-2' v-if='order.ordered_products.length>=2'>[ +{{order.ordered_products.length-1}} ]</span></p>
            </v-flex>

            <v-flex xs12 sm12 md4 lg3 xl3 class='date'>
                <p>
                    <v-icon small color='#1e1d2b' class='mr-1'>fas fa-calendar-alt</v-icon>
                    {{parseDate(order.order.order_on)}}kglkj
                </p>
            </v-flex>

            <v-flex xs12 sm12 md2 lg2 xl2 class='price'>
                <p>
                    <v-icon small color='#1e1d2b' class='mr-1'>fas fa-coins</v-icon>
                    {{order.paying}}
                </p>
            </v-flex>

            <v-flex xs12 sm12 md3 lg3 xl3 class='payment-method nav-layout hidden-md-and-down'>
                <p>
                    <v-icon small color='#1e1d2b' class='mr-1'>fas fa-credit-card</v-icon>
                    {{order.payment.method[0].name}}
                </p>
            </v-flex>

        </v-layout>
    </div>
</template>

<script>
export default {
    name: 'OrderTemp',

    props:['orderArr'],

    computed: {
    },

    data(){
        return{

        }
    },

    created(){
        console.log(this.orderArr[0].order);
    },

    methods: {
        parseDate(date){
            return new Date(date).toDateString()
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
   
</style>