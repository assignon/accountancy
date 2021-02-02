<template>
    <div class='details-core'>
        <div class='details-container'>
            <div class='product-details'>
                <h3>Product</h3>
                <p>Size: {{productDetails[0].products[0].tire[0].size}}</p>
                <p>Price: {{formatPrice(productDetails[0].products[0].tire[0].price)}}FRS</p>
                <p>Add on: {{productDetails[0].products[0].add_on}}</p>
                <p>Quantity: {{productDetails[0].products[0].tire[0].quantity}}</p>
                <p>Vehicule: {{productDetails[0].products[0].vehicle}}</p>
            </div>
            <div class='brands-details mt-5'>
                <h3>Brands</h3>
                <div class='brands'>
                    <p v-for='(brand, b) in productDetails[0].products[0].brands' :key="b">{{brand.name}}<span class='ml-2'></span></p>
                </div>
            </div>
            <div class='profiles-details'>
                <h3>Profiles</h3>
                <div class='profiles'>
                    <p v-for='(profile, p) in productDetails[0].products[0].profiles' :key="p">{{profile.name}}<span class='ml-2'></span></p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    name: 'ProductDetails',

     computed: {
        ...mapGetters({
            productDetails: 'product/getProductDetails',
        }),
    },

    data(){
        return {

        }
    },

    created() {
    },

    methods: {
        formatPrice(value) {
            let val = (value/1).toFixed(0).replace('.', ',')
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") 
        },
    }
}
</script>

<style scoped>
    .details-core{
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
    .product-details, .brands-details, .profiles-details{
        height: auto;
        width: 500px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .product-details h3, .brands-details h3, .profiles-details h3{
        color: white;
        margin-bottom: 10px;
    }
    .product-details p, .brands-details p, .profiles-details p{
        color: white;
        text-align: left;
        font-size: 15px;
        padding: 0px;
        margin: 0px;
        margin-bottom: 10px;
    }
</style>