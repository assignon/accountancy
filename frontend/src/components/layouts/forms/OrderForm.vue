<template>
    <v-form class="order-form animated" ref="orderForm">
        <p class='order-form-err-msg mb-5'></p>
        <div class='product-chips-container mt-3 mb-5'></div>
        <div class='products-fields'>
            <v-flex xs12 sm12 md6 lg6 xl6>
                <v-select
                    v-model="$store.state.order.product"
                    :rules="[$store.state.rules.required]"
                    :items="selectItemsArr"
                    label="Choose Product*"
                    outlined
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
            @click="updateStep(orderStep)"
          >
            <p style='font-size:17px;margin:auto;'>Next</p>
          </v-btn>
        </div>
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
            selectItemsArr: []
        }
    },
    created(){
        this.allProducts()
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

        createChip(name, title, price, entryIndex){
            console.log(name);
            let self = this;
            let productChipsContainer = document.querySelector('.product-chips-container');
            let chip = document.createElement('div');
            let chipTitle = document.createElement('p');
            let chipPrice = document.createElement('p');
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

            if(store.product != null && store.quantity != null && store.quantity > 0){
                // check if quality Criteria already exist in $store.state.ls.qualitycriteriaArr
                let chipExists = self.$store.state.order.productArr.findIndex(x => x.name ==  store.product);
                if(chipExists == -1){
                    // push
                    let currentEntry = {name: store.product, qty: store.quantity};
                    self.$store.state.order.productArr.push(currentEntry);
                    // create and add new quality Criteria chip
                    let currentEntryIndex = self.$store.state.order.productArr.indexOf(currentEntry);
                    let chip = self.createChip(randomName, store.product, store.quantity, currentEntryIndex);
                    console.log( self.$store.state.order.productArr);
                    // append chip to the DOM
                    productChipsContainer.appendChild(chip);
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
            if (store.product != null) {
                if(!document.body.contains(validationErrMsg)){
                    this.$emit('updatestep', stepNum)
                }else{
                    formErrMsg.innerHTML = validationErrMsg.textContent;
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
    .products-fields{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        /* margin-bottom: 20px;
        margin-top: 20px; */
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