<template>
    <div class='product-core'>
        <v-layout class='product-layout'>
            <div class='add-product'>
                <v-btn large @click='addProduct()' rounded color='#1976d2' class='mr-5'>Add Product</v-btn>
            </div>
            <div class='product-container' v-if='products[0].products.length>0'>
                <v-flex
                    xs12 sm12 md3 lg3 xl4
                    v-for="(product, i) in products[0].products"
                    :key="i"
                    class='prduct-flex animated'
                    :class='"product"+product.id'
                    
                >
                    <div class='product-inner-container'>
                        <div class='size'>
                            <!-- <h3>{{product.tire.size}} ({{formatPrice(product.tire.price)}}FRS)</h3> -->
                            <v-flex xs12 sm12 md8 lg8 xl8 style='display:flex;justify-content:flex-start;align-items:center;' @click='$store.state.infoDrawer=true, productDetails(product.id)'>
                                <h3>{{product.tire.size}}</h3>
                            </v-flex>
                            <v-flex xs12 sm12 md4 lg4 xl4 style='display:flex;flex-direction:row;justify-content:flex-end;align-items:center;'>
                                
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-icon  
                                            style='font-size:23px'
                                            v-bind="attrs"
                                            v-on="on"
                                            color='#0163d1' class='mr-4' 
                                            @click='productDetails(product.id), UpdateProduct()'
                                        >fas fa-edit</v-icon>
                                    </template>
                                    <span>Edit/add quantity</span>
                                </v-tooltip>

                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-icon  
                                            v-if='$session.get("warehouseName")!="all"'
                                            v-bind="attrs"
                                            v-on="on"
                                            style='font-size:23px'
                                            color='#0163d1' class='' 
                                            @click='$store.state.product.transferDialog=true, productDetails(product.id)'
                                        >fas fa-share-square</v-icon>
                                    </template>
                                    <span>Transfer</span>
                                </v-tooltip>
                                
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-icon  
                                            v-if='$session.get("su")'
                                            v-bind="attrs"
                                            v-on="on"
                                            style='font-size:23px'
                                            color='red' class='ml-3' 
                                            @click='removeDialog=true, productId=product.id'
                                        >fas fa-trash-alt</v-icon>
                                    </template>
                                    <span>Remove</span>
                                </v-tooltip>
                            </v-flex>
                        </div>
                        <div class='product-qty' @click='$store.state.infoDrawer=true, productDetails(product.id)'>
                            <h3 class='display-3 mt-3 font-weight-bold'>{{product.tire.quantity}}</h3>
                        </div>
                        <div class='brands' @click='$store.state.infoDrawer=true, productDetails(product.id)'>
                            <p v-for='(brand, b) in product.brands' :key="b">
                                <v-chip :ripple="false" small>
                                    {{brand.name}}<span class='ml-2'></span>
                                </v-chip>
                            </p>
                        </div>
                        <div class='profiles' @click='$store.state.infoDrawer=true, productDetails(product.id)'>
                            <p v-for='(profile, p) in product.profiles' :key="p">
                                <v-chip :ripple="false" small>
                                    {{profile.name}}<span class='ml-2'></span>
                                </v-chip>
                            </p>
                        </div>
                    </div>
                </v-flex>
            </div>
            <div class='no-product' v-else>
                <v-icon color='#15141c'>fas fa-boxes</v-icon>
                <h1>No products</h1>
            </div>
        </v-layout>
        <InformationModal 
            bColor='#15141c'    
            border='1px solid #15141c'
            closeClr='white' 
        />
        <TransferModal/>
         <!-- product remove confirmation dialog -->
        <v-dialog
            v-model="removeDialog"
            persistent
            max-width="600px"
        >   
            <div class='remove-dialog'>
                <p>Are you sure you want to delete this product?</p>
                <div class='btn-container'>
                    <v-btn mediun color="#1976d2" style='cursor:pointer;text-transform:capitalize' class='mr-3 pa-2' rounded @click="removeDialog=false"><span style='color:white'>No</span></v-btn>
                    <v-btn mediun color="red" style='cursor:pointer;text-transform:capitalize' class='pa-3' rounded @click="removeProduct()"><span style='color:white'>Yes</span></v-btn>
                </div>
            </div>
        </v-dialog>
    </div>
</template>

<script>
import InformationModal from "@/components/modals/InformationModal.vue";
import TransferModal from "@/components/modals/TransferModal.vue";
import { mapGetters } from 'vuex';
export default {
  name: "Order",
  
  components: {
       InformationModal,
       TransferModal
  },

    computed: {
        ...mapGetters({
            products: 'product/getProducts',
        }),
    },


  data(){
    return{
        removeDialog: false,
        productId: null,
    }
  },

  created(){
      this.allProducts()
      this.$store.state.infoDrawer = false
    //   let self = this;
    //   console.log(self.$store.state.product.productsArr.products);
  },

  methods: {
    allProducts(){
        let self = this;
        let store = self.$store;

        this.$store.dispatch("getReq", {
            url: "product/products",
            params: {
                date: null,
                user_id: this.$session.get('warehouseId')
            },
            auth: self.$session.get('token'),
            csrftoken: self.$session.get('token'),
            callback: function(data) {
                // console.log(data);
                store.getters["setData"]([store.state.product.productsArr, [data]]);
            },
        });
    },
    formatPrice(value) {
        let val = (value/1).toFixed(0).replace('.', ',')
        return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") 
    },

      addProduct(){
        this.$store.state.formsDialog = true;
        this.$store.state.product.addProductForm = true;
        this.$store.state.product.productProforma = false;
        this.$store.state.formName = ' Product';
        this.$store.state.formsTemp = 'ProductForm';
        this.$store.reload = true;
      },

      UpdateProduct(){
            this.$store.state.formsDialog = true;
            this.$store.state.product.addProductForm = false;
            this.$store.state.product.productProforma = false;
            this.$store.state.formName = ' Product';
            this.$store.state.formsTemp = 'ProductForm';
            this.$store.reload = true
      },

      removeProduct(){
        let self = this
        this.$store.dispatch("deleteReq", {
            url: "product/remove_product",
            params: {
                product_id: self.productId
            },
            auth: self.$session.get('token'),
            csrftoken: self.$session.get('token'),
            callback: function(data) {
                console.log(data);
                if(data.deleted){
                    alert(data.msg)
                    self.removeDialog = false
                    document.querySelector('.product'+self.productId).classList.add('fadeOutUp')
                    setTimeout(() => {
                         document.querySelector('.product'+self.productId).style.display = 'none'
                    }, 300)
                }else{
                    alert(data.msg)
                }
            },
        });
      },

      productDetails(productId){
        let self = this
        this.$store.dispatch("getReq", {
            url: "product/product_details",
            params: {
                product_id: productId
            },
            auth: self.$session.get('token'),
            csrftoken: self.$session.get('token'),
            callback: function(data) {
                console.log(data);
                self.$store.state.infoTempName = 'ProductDetails'
                self.$store.getters["setData"]([self.$store.state.product.productDetailsArr, [data]]);
            },
        });

      },
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
        background-color: #fff;
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
        flex-wrap: wrap;
        justify-content: center;
        align-items: flex-start;
        margin-top: 60px;
    }
    .prduct-flex{
        width: 250px;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        margin: 20px;
         /* box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px; */
    }
    .product-inner-container{
        height: 90%;
        width: 100%;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: flex-start;
        align-items: flex-start;
        border: 1px solid #ebf0f7;
        border-radius: 10px;
        background-color: #ebf0f7;
        padding: 30px;
        margin: 20px;
        /* box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px; */
        box-shadow: rgba(255, 255, 255, 0.2) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0.9) 0px 0px 0px 1px;
    }
    .size{
        height: auto;
        width: 90%;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .product-qty{
        height: auto;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    .product-qty h3{
        text-align: left;
    }
    .product-qty h3{
        text-align: center;
    }
    .brands, .profiles{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .no-product{
        width: 100%;
        height: 90vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .no-product .v-icon{
        font-size: 100px;
    }
    .remove-dialog{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: white;
        padding-top: 50px;
        padding-bottom: 50px;
    } 
    .btn-container{
        height: auto;
        width: 90%;
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        align-items: center;
    }
    @media only screen and (max-width: 500px){
        .product-core{
            width: 100%;
            margin-left: 0%;
        }
        .product-container{
            margin-top: 20px;
        }
        .prduct-flex{
            margin: 0px 10px 0px 10px;
        }
        .product-inner-container{
            margin: 0px;
        }
    }
</style>