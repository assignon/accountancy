<template>
    <v-form class="customerinfo-form animated fadeInUp" ref="customerInfoForm">
        <p class='form-err-msg'></p>
        <v-text-field
          v-model="$store.state.order.email"
          :rules="[$store.state.emailRules, $store.state.rules.required]"
          label="Email*"
          required
          outlined
          type="email"
        ></v-text-field>
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
          :rules="[$store.state.rules.required]"
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
    },
}
</script>

<style scoped>
    .customerinfo-form{
        width: 60%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
    .customerinfo-form .v-text-field{
         width: 100%;
     }
    .btn-container{
        width: 100%;
        height: auto;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
</style>