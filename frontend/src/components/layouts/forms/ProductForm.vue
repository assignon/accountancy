<template>
    <div class='product-form-core'>
        <v-form class="product-form animated" ref="productForm">
            <p class='mb-3'>
                Add New product to 
                <span style='color: #0163d1;font-weight:bold' v-if='Number($session.get("warehouseId"))==$session.get("userId") || $session.get("warehouseName")=="all"'>Main</span>
                <span style='color: #0163d1;font-weight:bold' v-else>{{$session.get('warehouseName')}}</span>
                warehouse
            </p>
            <p class='product-form-err-msg mb-5'></p>
            
            <div class='product-field-container'>
                <v-select
                    v-model="vehicle"
                    :items="selectVehicleArr"
                    :menu-props="{ bottom: true, offsetY: true }"
                    label="Select Vehicle*"
                    outlined
                    style='width=85%;'
                ></v-select>
                <v-icon 
                    style='font-size:50px;' 
                    color='#0163d1' 
                    @click='extraItemDialog=true,newExtra="vehicle"'
                    class='ml-5'
                >fas fa-plus-square</v-icon>
            </div>
            <div class='product-field-container'>
                <v-text-field
                    v-model="size"
                    :rules="[$store.state.rules.required]"
                    label="Size*"
                    required
                    outlined
                ></v-text-field>
            </div>
            <div class='product-field-container'>
                <v-text-field
                    v-model="price"
                    label="Price*"
                    type='number'
                    outlined
                ></v-text-field>
            </div>
            <div class='product-field-container' v-if="$store.state.product.productProforma==false">
                <v-text-field
                    v-model="quantity"
                    label="Quantity*"
                    type='number'
                    outlined
                ></v-text-field>
            </div>
            <div class='product-field-container'>
                <v-select
                    v-model="brands"
                    :items="selectBrandArr"
                    :menu-props="{ bottom: true, offsetY: true }"
                    label="Select Brands*"
                    multiple
                    chips
                    outlined
                    style='width=85%;'
                ></v-select>
                <v-icon 
                    style='font-size:50px;' 
                    color='#0163d1' 
                    @click='extraItemDialog = true, newExtra="brand"'
                    class='ml-5'
                >fas fa-plus-square</v-icon>
            </div>
            <div class='product-field-container'>
                <v-select
                    v-model="profiles"
                    :items="selectProfileArr"
                    :menu-props="{ bottom: true, offsetY: true }"
                    label="Select Profiles*"
                    multiple
                    chips
                    outlined
                    style='width=85%;'
                ></v-select>
                <v-icon 
                    style='font-size:50px;' 
                    color='#0163d1' 
                    @click='extraItemDialog = true, newExtra="profile"'
                    class='ml-5'
                >fas fa-plus-square</v-icon>
            </div>

            <div class="btn-container">
                <v-btn
                    depressed
                    height="50"
                    width="20%"
                    class="fot-weight-bold white--text"
                    color="#1976d2"
                    v-if='$store.state.product.addProductForm && $store.state.product.productProforma==false'
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
                    v-if='$store.state.product.addProductForm==false && $store.state.product.productProforma==false'
                    @click='submitUpdatedProduct()'
                >
                    <p style='font-size:17px;margin:auto;'>Update Product</p>
                </v-btn>
                <v-btn
                    large
                    depressed
                    height="50"
                    width="30%"
                    class="fot-weight-bold white--text"
                    color="#1976d2"
                    v-if='$store.state.product.productProforma && $store.state.product.addProductForm==false'
                    @click='createProforma()'
                >
                    <p style='font-size:17px;margin:auto;'>Create Proforma</p>
                </v-btn>
            </div>
        </v-form>
        <!-- add extra item dialog -->
        <v-dialog
            v-model="extraItemDialog"
            persistent
            max-width="600px"
        >
            <v-form class='new-extra'>
                <p class="headline mb-4">Add New {{newExtra}}</p>
                <v-spacer></v-spacer>
                <p class='new-extra-err mb-4'></p>
                <v-text-field
                    :label='newExtra'
                    required
                    outlined
                    :rules="[$store.state.rules.required]"
                    v-model='extraItemName'
                ></v-text-field>
                <v-spacer></v-spacer>
                <div class='btn-container'>
                    <v-btn
                        color="blue darken-1"
                        text
                        @click="extraItemDialog = false"
                    >
                        Close
                    </v-btn>
                    <v-btn
                    depressed
                        height="50"
                        width="20%"
                        class="fot-weight-bold white--text"
                        color="#1976d2"
                       @click="addExtra()"
                    >
                        <p style='font-size:17px;margin:auto;'>Add</p>
                    </v-btn>
                </div>
            </v-form>
        </v-dialog>

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
            products: 'product/getProducts',
        }),
       
    },
    data(){
        return{
            vehicle: null,
            size: null,
            price: 0,
            quantity: 1,
            selectVehicleArr: [],
            selectBrandArr: [],
            brands: [],
            selectProfileArr: [],
            profiles: [],
            extraItemDialog: false,
            extraItemName: null,
            newExtra: null,
        }
    },
    created(){
        this.allVehicles()
        this.allBrands()
        this.allProfiles()
        if(!this.$store.state.product.addProductForm && !this.$store.state.product.productProforma){
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
                    date: null,
                    user_id: this.$session.get('warehouseId')
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

        allVehicles(){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/vehicles",
                params: {
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log(JSON.parse(data));
                    JSON.parse(data).forEach(item => {
                        self.selectVehicleArr.push(item.fields.name)
                    })
                    store.getters["setData"]([store.state.product.vehiclesArr, JSON.parse(data)]);
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

        capitalizeFirstLetter(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        },

        addExtra(){
            // add extra profile, brand or vehicle
            let self = this;
            // let store = self.$store;
            
            let formErrMsg = document.querySelector(".new-extra-err");
            let validationErrMsg = document.querySelector('.v-messages__message');

            if(self.extraItemName != null && !document.body.contains(validationErrMsg)){
                let body = {
                    name: self.capitalizeFirstLetter(self.extraItemName)
                }
                if(self.newExtra == 'brand' && self.selectBrandArr.includes(self.capitalizeFirstLetter(self.extraItemName))){
                    formErrMsg.innerHTML = `This ${self.newExtra} already exists`;
                    return false
                }else if(self.newExtra == 'profile' && self.selectProfileArr.includes(self.capitalizeFirstLetter(self.extraItemName))){
                    formErrMsg.innerHTML = `This ${self.newExtra} already exists`;
                    return false
                }else if(self.newExtra == 'vehicle' && self.selectVehicleArr.includes(self.capitalizeFirstLetter(self.extraItemName))){
                    formErrMsg.innerHTML = `This ${self.newExtra} already exists`;
                    return false
                }

                self.$store.dispatch("postReq", {
                    url: `product/new_${self.newExtra}`,
                    params: body,
                    auth: self.$session.get('token'),
                    csrftoken: self.$session.get('token'),
                    callback: function(data) {
                        console.log(data);
                        if(data.added){
                            // add new extra to array
                            if(self.newExtra == 'brand'){
                                self.selectBrandArr.push(self.capitalizeFirstLetter(self.extraItemName))
                            }else if(self.newExtra == 'profile'){
                                self.selectProfileArr.push(self.capitalizeFirstLetter(self.extraItemName))
                            }else if(self.newExtra == 'vehicle'){
                                self.selectVehicleArr.push(self.capitalizeFirstLetter(self.extraItemName))
                            }
                            formErrMsg.innerHTML = data.msg
                             document.querySelector('.new-extra').reset()
                            //close dialog after 2sec
                            setTimeout(() => {
                                self.extraItemDialog = false
                                formErrMsg.innerHTML = ''
                            }, 2000)
                            setTimeout(() => {self.extraItemDialog = false}, 2000)
                        }else{
                            formErrMsg.innerHTML = data.msg
                        }
                    },
                });
            }else{
                formErrMsg.innerHTML = `Give the name of the ${self.newExtra}`;
            }
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
                price: self.price != null ? self.price : 0,
                quantity: self.quantity != null ? self.quantity : 1,
                vehicle: self.vehicle,
                brands: brandsPayload,
                profiles: profilesPayload,
                user_id: this.$session.get('warehouseId') == 0 ? this.$session.get('userId') : this.$session.get('warehouseId')
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
            if (
                // self.vehicle != null 
                self.size != null 
                // && self.brands.length > 0 
                // && self.profiles.length > 0
            ) {
                // if(self.price !=null && self.price > 0 && self.quantity != null && self.quantity > 0){
                    if(!document.body.contains(validationErrMsg)){
                        if(self.$store.state.product.addProductForm){
                            self.addProduct()
                        }else{
                            self.submitUpdatedProduct()
                        }
                    }else{
                        formErrMsg.innerHTML = validationErrMsg.textContent;
                    }
                // }else{
                //     formErrMsg.innerHTML = "Price and quantity should not be <= 0";
                // }
            } else {
                formErrMsg.innerHTML = "Field size required";
            }
        },

        createProforma(){
            let self = this;
            let store = self.$store.state.product

            self.$store.state.pdfTemp = 'ProformaPdf';
            self.$store.state.pdfDialog = true;

            store.proVehicle = self.vehicle
            store.proSize = self.size
            store.proPrice = self.price

            self.brands.forEach(item => {
                console.log(item);
                store.proBrands.push(item)
            })

            self.profiles.forEach(item => {
                store.proProfiles.push(item)
            })
            console.log(store.proBrands);
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
    .product-field-container{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .product-form .v-text-field{
         width: 85%;
     }
    .product-form-err-msg, .new-extra-err{
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
    .new-extra{
        width: 100%;
        height: auto;
        padding: 30px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        background-color: white;
    }
    .new-extra .v-text-field{
         width: 100%;
     }
</style>