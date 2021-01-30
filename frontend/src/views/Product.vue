<template>
    <div class='product-core'>
        <v-layout class='product-layout'>
            <div class='add-product'>
                <v-btn large @click='addProduct()' rounded color='#1976d2' class='mr-5'>Add Product</v-btn>
            </div>
            <div class='product-container'></div>
        </v-layout>
    </div>
</template>

<script>
// import InformationModal from "@/components/modals/InformationModal.vue";
import { mapGetters } from 'vuex';
export default {
  name: "Order",
  
  components: {
       
    },

    computed: {
        ...mapGetters({
            // orders: 'order/getOrders',
        }),
    },


  data(){
    return{
    }
  },

  created(){
    
  },

  methods: {
      addProduct(){
        this.$store.state.formsDialog = true;
        this.$store.state.formName = 'Product';
        // this.$store.state.formsTemp = 'OrderStepper';
      }
        // paymentDetails(customerid){
        //     let self = this;

        //     this.$store.dispatch('order/getPaymentDetails', {
        //         url: 'order/payment_details',
        //         params: {
        //             customerId: customerid
        //         },
        //         auth: self.$session.get('token'),
        //         csrftoken: self.$session.get('token'),
        //         callback: function(data){
        //             // console.log('api data', data);
        //             self.$store.state.infoTempName = 'PaymentDetails'
        //             self.$store.getters["setData"]([self.$store.state.order.customerPaymentArr, [data]]);
                    
        //         },
        //     })
        // },

        // newOrder(){
        //     this.$store.state.formsDialog = true;
        //     this.$store.state.formName = 'Order';
        //     this.$store.state.formsTemp = 'OrderStepper';
        // }
  }
};
</script>

<style scoped>
     .product-core{
        height: auto;
        width: 85%;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        margin-left: 15%;
        /* background-color: #1e1d2b; */
        background-color: #fafafa;
    }
    .product-layout{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: flex-start;
        padding-top: 30px;
    }
    .add-product{
        width: 100%;
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
    }
    .add-product .v-btn{
        color: #fff;
        font-size: 15px;
        font-weight: bolder;
        text-transform: capitalize;
    }
    .product-container{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: flex-start;
    }
</style>