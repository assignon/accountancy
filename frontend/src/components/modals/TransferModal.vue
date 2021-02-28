<template>
    <v-dialog
            v-model="$store.state.product.transferDialog"
            persistent
            max-width="600px"
        >
            <v-form class='transfer-form' ref='transferForm'>
                <!-- <h2 class='mb-3' style='text-align:left' v-if='$session.get("su")'>Transfer this product from </h2> -->
                <h2 class='mb-3'>
                    Transfer this product from 
                    <span style='color: #0163d1;font-weight:bold'>
                        {{$session.get('warehouseName') | suWarehouseName($session.get("su"), $session.get('warehouseName')) | capitalize($session.get('warehouseName'))}}
                    </span>
                    warehouse
                </h2>
                <p class='err-msg mb-4 mt-2' style='width:85%;'></p>
              
                <v-select
                    v-model="transferTo"
                    :rules="[$store.state.rules.required]"
                    :items="warehousesArr"
                    :menu-props="{ bottom: true, offsetY: true }"
                    label="Transfer To*"
                    outlined
                    style='width: 85%'
                    @click='getWarehouses'
                ></v-select>
                <v-text-field
                    v-model="qty"
                    :rules="[$store.state.rules.required]"
                    label="Quantity*"
                    required
                    type='number'
                    outlined
                ></v-text-field>

                <div class='details-container'>
                    <div class='product-details'>
                        <h3>Product</h3>
                        <p>Size: {{productDetails[0].products[0].tire[0].size}}</p>
                        <p>Price: {{formatPrice(productDetails[0].products[0].tire[0].price)}}FRS</p>
                        <p>Add on: {{productDetails[0].products[0].add_on}}</p>
                        <p>Quantity: {{productDetails[0].products[0].tire[0].quantity}}</p>
                        <p>Vehicule: {{productDetails[0].products[0].vehicle}}</p>
                    </div>
                    <div class='brands-details'>
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

                <div class='btn-container'>
                    <v-btn large @click='$store.state.product.transferDialog=false' color='#1976d2' class='mr-3'>close</v-btn>
                    <v-btn large @click='transferProduct()' color='#1976d2'>Tranfer Product</v-btn>
                </div>
            </v-form>
        </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    name: 'ProductTransferModal',

    computed: {
        ...mapGetters({
            productDetails: 'product/getProductDetails',
            warehouses: 'dashboard/getWarehouse',
        }),
    },

    filters: {
        suWarehouseName: function(name, su){
            if(!su) return name
            name = 'main'
            return name
        }, 
        capitalize: function (value) {
            if (!value) return ''
            value = value.toString()
            return value.charAt(0).toUpperCase() + value.slice(1)
        }
    },

    data(){
        return{
            warehousesArr: [],
            transferTo: null,
            qty: 0
        }
    },

    created(){
        let self = this

        this.getWarehouses()
        
        setTimeout(() => {
            this.warehouses[0].forEach(items => {
                self.warehousesArr.push(items.name)
            })
            this.excludeCurrentWarehouseFromArr()
        }, 100);
    },

    methods: {
        excludeCurrentWarehouseFromArr(){
            let self = this
            let currentWh = this.$session.get('su') ? 'main' : this.$session.get('warehouseName')

            let currentWhIndex = self.warehousesArr.findIndex(x => x == currentWh);
            if(currentWhIndex != -1){
                self.warehousesArr.splice(currentWhIndex, 1);
            }

            // self.warehousesArr.filter(function(value, index, arr){ 
            //     console.log(index, value, arr);
            //     return value == currentWh;
            // });
        },

        formatPrice(value) {
            let val = (value/1).toFixed(0).replace('.', ',')
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") 
        },

        getWarehouses(){
            let self = this;

            self.$store.dispatch("getReq", {
                url: 'dashboard/get_warehouses',
                params: {},
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log(data);
                    self.$store.getters["setData"]([self.$store.state.dashboard.warehouseArr, [data]]);
                    console.log(self.$store.state.dashboard.warehouseArr);
                },
            });
        },

        transferProduct(){
            let self = this
            let formErrMsg = document.querySelector(".err-msg");
            let validationErrMsg = document.querySelector('.v-messages__message');

            if(
                self.transferTo != null &&
                self.qty != null &&
                !document.body.contains(validationErrMsg)
            ){
                if(self.qty > 0 && self.qty <= self.productDetails[0].products[0].tire[0].quantity){
                    formErrMsg.innerHTML = ''
                    let brandsPayload = {
                        brands: self.productDetails[0].products[0].brands
                    }
                    let profilesPayload = {
                        profiles: self.productDetails[0].products[0].profiles
                    }
                    let body = {
                        sender_id: self.$session.get('userId'),
                        receiver_name: self.transferTo,
                        size: self.productDetails[0].products[0].tire[0].size,
                        price: self.productDetails[0].products[0].tire[0].price,
                        vehicle: self.productDetails[0].products[0].vehicle,
                        qty: self.qty,
                        brands: brandsPayload,
                        profiles: profilesPayload,
                    }
                    // send request
                    this.$store.dispatch("postReq", {
                        url: "product/transfer_product",
                        params: body,
                        auth: self.$session.get('token'),
                        csrftoken: self.$session.get('token'),
                        callback: function(data) {
                            console.log('transfer',data);
                            if(data.transfered){
                                formErrMsg.innerHTML = 'Product tranfered'
                                document.querySelector('.transfer-form').reset()
                                //close dialog after 2sec
                                setTimeout(() => {
                                    self.$store.state.product.transferDialog = false
                                    formErrMsg.innerHTML = ''
                                    // window.location.reload()
                                }, 2000)
                            }else{
                                formErrMsg.innerHTML = 'Something went wrong, try to reload the page and try again'
                            }
                        },
                    });
                }else{
                    formErrMsg.innerHTML = 'Product quantity should not be 0 and should not be greater than the quantity available in the sender warehouse'
                }
            }else{
                formErrMsg.innerHTML = 'Select the destination warehouse and product quantity should not be empty'
            }
        }
    }
}
</script>

<style scoped>
    .transfer-form{
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
    .err-msg{
        text-align: center;
        font-size: 17px;
        color: #ce2b58;
    }
    .transfer-form .v-text-field{
        width: 85%;
    }
    .details-container{
        height: 85%;
        width: 85%;
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
        color: #15141c;
        margin-bottom: 10px;
    }
    .product-details p, .brands-details p, .profiles-details p{
        color: #15141c;
        text-align: left;
        font-size: 15px;
        padding: 0px;
        margin: 0px;
        margin-bottom: 10px;
    }  
    .btn-container{
        height: auto;
        width: 85%;
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        align-items: flex-end;
    }
    .btn-container .v-btn{
        color: #fff;
        font-size: 15px;
        font-weight: bolder;
        text-transform: capitalize;
    }
    .btn-container p{
        text-align: right;
        font-size: 17px;
        font-weight: bolder;
        cursor: pointer;
        color: #1976d2;
    }
</style>