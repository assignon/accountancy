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
                <h3>Product</h3>
                <p>Size: {{productDetails[0].products[0].tire[0].size}}</p>
                <p>Price: {{productDetails[0].products[0].tire[0].price}}</p>
                <p>Add on: {{productDetails[0].products[0].add_on}}</p>
                <p>Quantity: {{productDetails[0].products[0].tire[0].quantity}}</p>
                <p>Vehicule: {{productDetails[0].products[0].vehicle}}</p>
            </div>

            <div class='payment-flex'>
                <h3>Brands</h3>
                <div class='brands'>
                    <p v-for='(brand, b) in productDetails[0].products[0].brands' :key="b">{{brand.name}}<span class='ml-2'></span></p>
                </div>
            </div>
        </div>
        <div class='divider'></div>
        <div class='pdf-footer'>
             <h3>Profiles</h3>
            <div class='profiles'>
                <p v-for='(profile, p) in productDetails[0].products[0].profiles' :key="p">{{profile.name}}<span class='ml-2'></span></p>
            </div>
            <div class='total-price'>
                <v-btn large color='#1976d2' style='position:relative;top:70px;color:white;text-transform:capitalize;font-weight:bold;' @click='printOrder()'>Print PDF</v-btn>
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
            productDetails: 'product/getProductDetails',
        }),
    },

    created(){
    },

    methods: {
        printOrder(){
            // this.$emit('printOrder')
            window.print();
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
        height: auto;
        overflow: hidden;
        padding: 30px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        background-color: #fff;
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