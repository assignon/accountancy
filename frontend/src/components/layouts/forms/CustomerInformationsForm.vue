<template>
    <v-form class="customerinfo-form animated fadeInUp" ref="customerInfoForm">
        <p class='form-err-msg'></p>
        <div class='customer-founded-container'>
            <v-text-field
                v-model="$store.state.order.email"
                :rules="[$store.state.rules.required]"
                label="Email*"
                required
                outlined
                type="email"
                @input='getCredentials()'
            ></v-text-field>
            <p class='customer-founded'></p>
        </div>
        <v-text-field
          v-model="$store.state.order.name"
          :rules="[$store.state.rules.required]"
          label="Name*"
          required
          outlined
        ></v-text-field>
         <v-text-field
          v-model="$store.state.order.telNumber"
          :rules="[$store.state.rules.required]"
          label="TelNumber*"
          required
          outlined
        ></v-text-field>
        <v-text-field
          v-model="$store.state.order.address"
          label="Address"
          required
          outlined
        ></v-text-field>


        <div class="btn-container">
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
    name: 'CustomerInfoForm',
    props: ["orderStep"],
    computed: {
        ...mapGetters({
                // categories: "ls/getCategories",
        }),
    },

    data(){
        return{
            
        }
    },
    
    created(){},

    methods: {
        updateStep(stepNum){
            let self = this;
            let store = self.$store.state.order;
            let formErrMsg = document.querySelector(".form-err-msg");
            let validationErrMsg = document.querySelector('.v-messages__message');

            if (store.email != null && store.name != null && store.telNumber != null) {
                if(!document.body.contains(validationErrMsg)){
                    this.$emit('updatestep', stepNum)
                }else{
                    formErrMsg.innerHTML = validationErrMsg.textContent;
                }
            } else {
                formErrMsg.innerHTML = "Fields are empty";
            }
        },

        getCredentials(){
            let email = this.$store.state.order.email
            let regexEmail =/\S+@\S+\.\S+/;
            let self = this;
            let customerFounded = document.querySelector('.customer-founded')
            let store = this.$store.state.order

            if(regexEmail.test(email)){

                this.$store.dispatch("getReq", {
                    url: "customer/credentials_form_auto_fill",
                    params: {
                        email: email
                    },
                    auth: self.$session.get('token'),
                    csrftoken: self.$session.get('token'),
                    callback: function(data) {
                        console.log(data);
                        if(data.founded){
                            customerFounded.innerHTML = 'Email credentials founds'
                            store.email = data.credentials[0].email;
                            store.name = data.credentials[0].name;
                            store.address = data.credentials[0].address;
                            store.telNumber = data.credentials[0].tel_number;
                        }
                        // store.getters["setData"]([store.state.product.productsArr, [data]]);
                    },
                });
            }
        }
    },
}
</script>

<style scoped>
    .customerinfo-form{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .customerinfo-form .v-text-field{
         width: 60%;
     }
     .customer-founded-container{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
     }
     .customer-founded-container p{
         width: 40%;
         height: auto;
         font-size: 15px;
         text-align: left;
         margin-left: 20px;
         position: relative;
         top: 10px;
     }
    .btn-container{
        width: 60%;
        height: auto;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
</style>