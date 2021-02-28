<template>
    <v-form class="order-form animated" ref="orderForm">
        <p class='order-form-err-msg mb-5'></p>
        <div class='product-chips-container mt-3 mb-5'></div>

        <div class='order-field-container'>
            <v-select
                v-model="$store.state.order.vehicule"
                :items="vehiculeItemsArr"
                :menu-props="{ bottom: true, offsetY: true }"
                label="Choose Vehicle*"
                outlined
                style='width: 100%'
                @change='filteredProducts()'
            ></v-select>
            <v-icon 
                style='font-size:50px;' 
                color='#0163d1' 
                @click='addNewProduct'
                class='ml-5'
            >fas fa-plus-square</v-icon>
        </div>
        
        <div class='brands-profiles-select'>
            <div class='order-field-container'>
                <v-flex xs12 sm12 md11 lg11 xl11>
                    <v-select
                        v-model="$store.state.order.brands"
                        :items="brandsItemsArr"
                        :menu-props="{ bottom: true, offsetY: true }"
                        label="Choose Brands*"
                        outlined
                        chips
                        multiple
                        @change='filteredProducts()'
                    ></v-select>
                </v-flex>
                <v-icon 
                    style='font-size:50px;' 
                    color='#0163d1' 
                    @click='addNewProduct'
                    class='ml-5 mr-2'
                >fas fa-plus-square</v-icon>
            </div>
            <div class='order-field-container'>
                <v-flex xs12 sm12 md12 lg12 xl12>
                    <v-select
                        v-model="$store.state.order.profiles"
                        :items="profileItemsArr"
                        :menu-props="{ bottom: true, offsetY: true }"
                        label="Choose profiles*"
                        outlined
                        multiple
                        chips
                        @change='filteredProducts()'
                    ></v-select>
                </v-flex>
                <v-icon 
                    style='font-size:50px;' 
                    color='#0163d1' 
                    @click='addNewProduct'
                    class='ml-5'
                >fas fa-plus-square</v-icon>
            </div>
        </div>

        <div class='products-fields'>
            <v-flex xs12 sm12 md6 lg6 xl6>
                <v-select
                    v-model="$store.state.order.product"
                    :rules="[$store.state.rules.required]"
                    :items="selectItemsArr"
                    :menu-props="{ bottom: true, offsetY: true }"
                    label="Choose Product*"
                    outlined
                    @click='filteredProducts()'
                ></v-select>
            </v-flex>
            <v-flex xs12 sm12 md2 lg2 xl2>
                <v-text-field
                    v-model="$store.state.order.quantity"
                    :rules="[$store.state.rules.required]"
                    label="Quantity*"
                    type="number"
                    required
                    outlined
                ></v-text-field>
            </v-flex>

            <v-flex xs12 sm12 md3 lg3 xl3>
                <v-btn
                    depressed
                    height="55"
                    width="100%"
                    class="fot-weight-bold white--text mr-2"
                    color="#1976d2"
                    v-if='$store.state.order.product != null'
                    @click="addProduct()"
                >
                    Add product
                </v-btn>
            </v-flex>
        </div>
        
        <div class="btn-container">
          <v-btn
                depressed
                height="50"
                width="20%"
                class="fot-weight-bold white--text mr-2"
                color="#1976d2"
                @click="updatePreviousStep(orderStep)"
          >
            <p style='font-size:17px;margin:auto;'>Previous</p>
          </v-btn>

          <v-btn
            depressed
            height="50"
            width="20%"
            class="fot-weight-bold white--text"
            color="#1976d2"
            :disabled='productNotAdded'
            @click="updateStep(orderStep)"
          >
            <p style='font-size:17px;margin:auto;'>Next</p>
          </v-btn>
        </div>
         <!-- add extra item dialog -->
        <!-- <v-dialog
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
        </v-dialog> -->
    </v-form>
</template>

<script>
import { mapGetters } from "vuex";
export default {
    name: 'OrderForm',

    props: ["orderStep"],

    computed: {
        ...mapGetters({
            products: 'product/getProducts',
        }),
       
    },
    data(){
        return{
            selectItemsArr: [],
            brandsItemsArr: [],
            vehiculeItemsArr: [],
            profileItemsArr: [],
            productNotAdded: true,
            productIsNull: true,
            extraItemDialog: false,
            extraItemName: null,
            newExtra: null,
        }
    },
    created(){
        // this.allProducts()
        this.allBrands()
        this.allProfiles()
        this.allVehicles()
    },

    methods: {
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
                        self.vehiculeItemsArr.push(item.fields.name)
                    })
                    store.getters["setData"]([store.state.product.vehiclesArr, JSON.parse(data)]);
                },
            });
        },

        capitalizeFirstLetter(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        },

        addNewProduct(){
            this.$store.state.formsDialog = true;
            this.$store.state.product.addProductForm = true;
            this.$store.state.formName = ' Product';
            this.$store.state.formsTemp = 'ProductForm';
            this.$store.reload = false;
        },

        //  addExtra(){
        //     // add extra profile, brand or vehicle
        //     let self = this;
        //     // let store = self.$store;
            
        //     let formErrMsg = document.querySelector(".new-extra-err");
        //     // let validationErrMsg = document.querySelector('.v-messages__message');

        //     if(self.extraItemName != null){
        //         let body = {
        //             name: self.capitalizeFirstLetter(self.extraItemName)
        //         }

        //         if(self.newExtra == 'brand' && self.brandsItemsArr.includes(self.capitalizeFirstLetter(self.extraItemName))){
        //             formErrMsg.innerHTML = `This ${self.newExtra} already exists`;
        //             return false
        //         }else if(self.newExtra == 'profile' && self.profileItemsArr.includes(self.capitalizeFirstLetter(self.extraItemName))){
        //             formErrMsg.innerHTML = `This ${self.newExtra} already exists`;
        //             return false
        //         }else if(self.newExtra == 'vehicle' && self.vehiculeItemsArr.includes(self.capitalizeFirstLetter(self.extraItemName))){
        //             formErrMsg.innerHTML = `This ${self.newExtra} already exists`;
        //             return false
        //         }

        //         self.$store.dispatch("postReq", {
        //             url: `product/new_${self.newExtra}`,
        //             params: body,
        //             auth: self.$session.get('token'),
        //             csrftoken: self.$session.get('token'),
        //             callback: function(data) {
        //                 console.log(data);
        //                 if(data.added){
        //                     // add new extra to array
        //                     if(self.newExtra == 'brand'){
        //                         self.brandsItemsArr.push(self.capitalizeFirstLetter(self.extraItemName))
        //                     }else if(self.newExtra == 'profile'){
        //                         self.profileItemsArr.push(self.capitalizeFirstLetter(self.extraItemName))
        //                     }else if(self.newExtra == 'vehicle'){
        //                         self.vehiculeItemsArr.push(self.capitalizeFirstLetter(self.extraItemName))
        //                     }
        //                     formErrMsg.innerHTML = data.msg
        //                     self.extraItemName = ''
        //                     formErrMsg.innerHTM = ''
        //                     //close dialog after 2sec
        //                     setTimeout(() => {self.extraItemDialog = false}, 2000)
        //                 }else{
        //                     formErrMsg.innerHTML = data.msg
        //                 }
        //             },
        //         });
        //     }else{
        //         formErrMsg.innerHTML = `Give the name of the ${self.newExtra}`;
        //     }
        // },

        filteredProducts(){
            let self = this;
            let store = self.$store;
          
            let brandsPayload = {
                brands: store.state.order.brands
            }
            let profilesPayload = {
                profiles: store.state.order.profiles
            }
             self.selectItemsArr = [];
             store.state.order.product = null

            // if(
            //     store.state.order.vehicule != null 
            //     && store.state.order.brands.length > 0 
            //     && store.state.order.profiles.length > 0
            // ){
            this.$store.dispatch("getReq", {
            url: "product/filter_products",
            params: {
                vehicle: store.state.order.vehicule,
                brands: brandsPayload,
                profiles: profilesPayload,
                user_id: self.$session.get('userId')
            },
            auth: self.$session.get('token'),
            csrftoken: self.$session.get('token'),
            callback: function(data) {
                console.log(data);
                data.tire.forEach(item => {
                    self.selectItemsArr.push(item.size+'-'+item.quantity)
                })
                store.getters["setData"]([store.state.product.filteredProductsArr, [data]]);
                },
            });
            // }
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
                        self.brandsItemsArr.push(item.fields.name)
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
                        self.profileItemsArr.push(item.fields.name)
                    })
                    store.getters["setData"]([store.state.product.ProfilesArr, JSON.parse(data)]);
                },
            });
        },

        createChip(name, title, price,vehicule, brands, profiles, entryIndex){
            console.log(name);
            let self = this;
            let productChipsContainer = document.querySelector('.product-chips-container');
            let chip = document.createElement('div');
            let chipTitle = document.createElement('p');
            let chipPrice = document.createElement('p');
            let chipVehicule = document.createElement('p');
            let chipBrands = document.createElement('p');
            let chipProfiles = document.createElement('p');
            let icon = document.createElement('i');

            chip.className = `ma-2 pl-3 pr-3 pb-2 pt-2 animated fadeInUp`;
            chip.id = entryIndex;
            chip.style.borderRadius = '100px';
            chip.style.backgroundColor = '#15141c';
            chip.style.display = 'flex';
            chip.style.flexDirection = 'row';
            chip.style.justifyContent = 'center';
            chip.style.alignItems = 'center';

            chipTitle.textContent = title;
            chipTitle.style.textAlign = 'center';
            chipTitle.style.fontSize = '15px';
            chipTitle.style.margin = 'auto';
            chipTitle.style.color = 'white';

            chipVehicule.textContent = '['+vehicule+']';
            chipVehicule.style.textAlign = 'center';
            chipVehicule.style.fontSize = '15px';
            chipVehicule.style.margin = 'auto';
            chipVehicule.style.color = 'white';

            chipBrands.textContent = '['+brands+']';
            chipBrands.style.textAlign = 'center';
            chipBrands.style.fontSize = '15px';
            chipBrands.style.margin = 'auto';
            chipBrands.style.color = 'white';

            chipProfiles.textContent = '['+profiles+']';
            chipProfiles.style.textAlign = 'center';
            chipProfiles.style.fontSize = '15px';
            chipProfiles.style.margin = 'auto';
            chipProfiles.style.color = 'white';

            chipPrice.textContent = ' ( '+price+' ) ';
            chipPrice.style.textAlign = 'center';
            chipPrice.style.fontSize = '15px';
            chipPrice.style.margin = 'auto';
            chipPrice.style.color = 'white';

            icon.className = 'fas fa-times pr-2'
            icon.style.fontSize = '15px';
            icon.style.position = 'relative';
            icon.style.left = '8px';
            icon.style.cursor = 'pointer';
            icon.style.color = 'white';

            chip.appendChild(chipTitle)
            chip.appendChild(chipBrands)
            chip.appendChild(chipVehicule)
            chip.appendChild(chipProfiles)
            chip.appendChild(chipPrice)
            chip.appendChild(icon)

            icon.addEventListener('click', function(e){
                self.$store.state.order.productArr.splice(chip.id, 1);
                e.currentTarget.parentNode.style.display = 'none';
                e.currentTarget.parentNode.remove();
                 if(chip.id != 0){
                    chip.id -= 1
                }
                if(productChipsContainer.children.length == 0){
                    self.$store.state.order.productArr = []
                }
                console.log(chip);
            })

            return chip;
        },

        addProduct(){
            let productChipsContainer = document.querySelector('.product-chips-container');
            let formErrMsg = document.querySelector(".order-form-err-msg");
            let self = this;
            let store = self.$store.state.order;
            let randomName = self.$store.getters["getRandomString"](5);
            let brandExistsArr = [];
            let profileExistsArr = [];

            if(store.product != null && store.quantity != null && store.quantity > 0){
                let productSize = store.product.split('-')
                // check if quality Criteria already exist in $store.state.ls.qualitycriteriaArr
                let chipExists = self.$store.state.order.productArr.findIndex(x => x.name ==  productSize[0]);
                // let chiQtypExists = self.$store.state.order.productArr.findIndex(x => x.qty ==  store.quantity);

                let vehiculeExists = self.$store.state.order.productArr.findIndex(x => x.vehicule ==  store.vehicule);
        
                store.brands.forEach(b => {
                    let brandExists = self.$store.state.order.productArr.findIndex(x => x.brand ==  b);
                    if(brandExists != -1){
                       brandExistsArr.push(true)
                    } else{
                       brandExistsArr.push(false)     
                    }
                    
                })
                store.profiles.forEach(p => {
                    let profileExists = self.$store.state.order.productArr.findIndex(x => x.profile ==  p);
                    if(profileExists != -1){
                       profileExistsArr.push(true)
                    } else{
                       profileExistsArr.push(false)     
                    }
                })
                console.log(brandExistsArr);
                // one false = add
                if(
                    chipExists == -1 
                    || 
                    brandExistsArr.includes(false) ||
                    profileExistsArr.includes(false) || 
                    vehiculeExists == -1 
                ){
                    // push
                    let currentEntry = {
                        name: productSize[0], 
                        qty: store.quantity, 
                        brand: [...store.brands], 
                        profile: [...store.profiles], 
                        vehicule: store.vehicule
                    };
                    self.$store.state.order.productArr.push(currentEntry);
                    // create and add new quality Criteria chip
                    let currentEntryIndex = self.$store.state.order.productArr.indexOf(currentEntry);
                    
                    let chip = self.createChip(
                        randomName, 
                        productSize[0], 
                        store.quantity, 
                        store.vehicule, 
                        [...store.brands], 
                        [...store.profiles], 
                        currentEntryIndex
                    );
                    
                    // append chip to the DOM
                    productChipsContainer.appendChild(chip);
                    self.productNotAdded = false
                    // # empy form
                    // store.brands.length = 0
                    // store.profiles.length = 0
                    // store.vehicule = null
                    // store.product = null
                    brandExistsArr.length = 0
                    profileExistsArr.length = 0
                    // console.log( self.$store.state.order.productArr);
                }else{
                    formErrMsg.innerHTML = "Product already added";
                }
            }else{
                formErrMsg.innerHTML = "Fields are empty or quantity is 0";
            }
        },

        updateStep(stepNum){
            let self = this;
            let store = self.$store.state.order;
            let formErrMsg = document.querySelector(".order-form-err-msg");
            let validationErrMsg = document.querySelector('.v-messages__message');

            if (store.product != null && store.quantity > 0) {
                let productSize = store.product.split('-')
                store.product  = productSize[0]
                let productEnough = Number(productSize[1]) > Number(store.quantity)
                if(productEnough){
                    if(!document.body.contains(validationErrMsg)){
                        this.$emit('updatestep', stepNum)
                    }else{
                        formErrMsg.innerHTML = validationErrMsg.textContent;
                    }
                }else{
                    alert(`The quantity ordered (${store.quantity}) is greater than the quantity of product in stock (${productSize[1]})`)
                }
            } else {
                formErrMsg.innerHTML = "Fields are empty";
            }
        },

        updatePreviousStep(stepNum){
            this.$emit('updateprevstep', stepNum)
        },
    },
}
</script>

<style scoped>
    .order-form{
        width: 70%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
    /* .order-form .v-text-field{
         width: 100%;
     } */
     .product-chips-container{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-around;
        align-items: flex-start;
        padding: 15px;
        border: 1px solid gray;
        border-radius: 3px;
        /* margin-bottom: 10px; */
    }
    .form-err-msg{
        width: 100%;
        height: auto;
        text-align: left;
        color: #15141c;
        font-size: 15px;
    }
    .products-fields, .brands-profiles-select{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        /* margin-bottom: 20px;
        margin-top: 20px; */
    }
    .order-field-container{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
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