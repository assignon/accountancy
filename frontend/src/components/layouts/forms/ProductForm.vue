<template>
    <div class='product-form-core'>
        <v-form class="product-form animated" ref="productForm">
            <p class='product-form-err-msg mb-5'></p>
            
            <v-select
                v-model="vehicle"
                :rules="[$store.state.rules.required]"
                :items="selectVehicleArr"
                label="Select Vehicle*"
                outlined
            ></v-select>
            <v-text-field
                v-model="size"
                :rules="[$store.state.rules.required]"
                label="Size*"
                required
                outlined
            ></v-text-field>
            <v-text-field
                v-model="price"
                :rules="[$store.state.rules.required]"
                label="Price*"
                type='number'
                required
                outlined
            ></v-text-field>
            <v-text-field
                v-model="quantity"
                :rules="[$store.state.rules.required]"
                label="Quantity*"
                type='number'
                required
                outlined
            ></v-text-field>
            <v-select
                v-model="brands"
                :rules="[$store.state.rules.required]"
                :items="selectBrandArr"
                label="Select Brands*"
                multiple
                chips
                outlined
            ></v-select>
            <v-select
                v-model="profiles"
                :rules="[$store.state.rules.required]"
                :items="selectProfileArr"
                label="Select Profiles*"
                multiple
                chips
                outlined
            ></v-select>
            
            <div class="btn-container">
                <v-btn
                    depressed
                    height="50"
                    width="20%"
                    class="fot-weight-bold white--text"
                    color="#1976d2"
                    v-if='$store.state.product.addProductForm'
                    @click='submitProduct()'
                >
                    <p style='font-size:17px;margin:auto;'>Add Product</p>
                </v-btn>
                 <v-btn
                    large
                    depressed
                    height="50"
                    width="30%"
                    class="fot-weight-bold white--text"
                    color="#1976d2"
                    v-else
                    @click='submitUpdatedProduct()'
                >
                    <p style='font-size:17px;margin:auto;'>Update Product</p>
                </v-btn>
            </div>
        </v-form>
    </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
    name: 'ProductForm',

    props: [],

    computed: {
        ...mapGetters({
            productDetails: 'product/getProductDetails',
            // products: 'product/getProducts',
        }),
       
    },
    data(){
        return{
            vehicle: null,
            size: null,
            price: null,
            quantity: null,
            selectVehicleArr: ['Car', 'Truck'],
            selectBrandArr: [],
            brands: [],
            selectProfileArr: [],
            profiles: [],
        }
    },
    created(){
        this.allBrands()
        this.allProfiles()
        if(!this.$store.state.product.addProductForm){
            setTimeout(() => {
                this.fillProductForm()
            },200)
        }
    },

    methods: {
        allProducts(){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/products",
                params: {
                    date: null
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    data.tire.forEach(item => {
                        self.selectItemsArr.push(item.size)
                    })
                    store.getters["setData"]([store.state.product.productsArr, [data]]);
                },
            });
        },

        allBrands(){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/brands",
                params: {
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log(JSON.parse(data));
                    JSON.parse(data).forEach(item => {
                        self.selectBrandArr.push(item.fields.name)
                    })
                    store.getters["setData"]([store.state.product.BrandssArr, JSON.parse(data)]);
                },
            });
        },

        allProfiles(){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/profiles",
                params: {
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log(JSON.parse(data));
                    JSON.parse(data).forEach(item => {
                        self.selectProfileArr.push(item.fields.name)
                    })
                    store.getters["setData"]([store.state.product.ProfilesArr, JSON.parse(data)]);
                },
            });
        },

        productsDetails(productId){
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

        addProduct(){
            let self = this
            let brandsPayload = {
                brands: self.brands
            }
            let profilesPayload = {
                profiles: self.profiles
            }
            let body = {
                size: self.size,
                price: self.price,
                quantity: self.quantity,
                vehicle: self.vehicle,
                brands: brandsPayload,
                profiles: profilesPayload
            }

            this.$store.dispatch("postReq", {
                url: "product/new_product",
                params: body,
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    console.log('added',data);
                    if(data.created){
                        // window.location.reload();
                        self.productsDetails(data.product_id)
                        self.$store.state.pdfTemp = 'ProductPdf';
                        self.$store.state.pdfDialog = true;
                    }
                },
            });
        },

        submitProduct(){
            let self = this;
            let formErrMsg = document.querySelector(".product-form-err-msg");
            let validationErrMsg = document.querySelector('.v-messages__message');
            console.log(self.vehicle);
                        console.log(self.profiles);
            if (self.vehicle != null 
                && self.size != null 
                && self.brands.length > 0 
                && self.profiles.length > 0
            ) {
                if(self.price !=null && self.price > 0 && self.quantity != null && self.quantity > 0){
                    if(!document.body.contains(validationErrMsg)){
                        if(self.$store.state.product.addProductForm){
                            self.addProduct()
                        }else{
                            self.submitUpdatedProduct()
                        }
                    }else{
                        formErrMsg.innerHTML = validationErrMsg.textContent;
                    }
                }else{
                    formErrMsg.innerHTML = "Price and quantity should not be <= 0";
                }
            } else {
                formErrMsg.innerHTML = "Fields are empty";
            }
        },

        fillProductForm(){
            let self = this;

            self.vehicle = self.productDetails[0].products[0].vehicle
            self.size = self.productDetails[0].products[0].tire[0].size
            self.price = self.productDetails[0].products[0].tire[0].price
            self.quantity = self.productDetails[0].products[0].tire[0].quantity

            self.productDetails[0].products[0].brands.forEach(item => {
                self.brands.push(item.name)
            })

            self.productDetails[0].products[0].profiles.forEach(item => {
                self.profiles.push(item.name)
            })
        },

        submitUpdatedProduct(){
            let self = this
            let brandsPayload = {
                brands: self.brands
            }
            let profilesPayload = {
                profiles: self.profiles
            }
            let body = {
                size: self.size,
                price: self.price,
                quantity: self.quantity,
                vehicle: self.vehicle,
                brands: brandsPayload,
                profiles: profilesPayload,
                tire_id: self.productDetails[0].products[0].tire[0].id
            }

            this.$store.dispatch("putReq", {
                url: "product/update_product",
                params: body,
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    console.log('added',data);
                    if(data.updated){
                        self.productsDetails(data.product_id)
                        self.$store.state.pdfTemp = 'ProductPdf';
                        self.$store.state.pdfDialog = true;
                    }
                },
            });
        }
    },
}
</script>

<style scoped>
    .product-form-core{
        width: 100%;
        height: auto;
        min-height: 94%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: #fffafa;
        padding-bottom: 10px;
    }
    .product-form{
        width: 50%;
        height: auto;
        min-height: 94%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
    .product-form .v-text-field{
         width: 100%;
     }
    .product-form-err-msg{
        width: 100%;
        height: auto;
        text-align: left;
        color: #15141c;
        font-size: 15px;
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