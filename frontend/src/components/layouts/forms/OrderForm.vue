<template>
    <v-form class="order-form animated" ref="orderForm">
        <p class='form-err-msg'></p>
        <v-text-field
          v-model="$store.state.order.what"
          :rules="[$store.state.rules.required]"
          label="What*"
          required
          outlined
          data-aos="fade-up"
          data-aos-delay="150"
          data-aos-duration="500"
        ></v-text-field>
        <v-select
          v-model="$store.state.ls.category"
          :rules="[$store.state.rules.required]"
          :items="categories"
          label="Choose category"
          outlined
          :disabled='categoryDisable'
        ></v-select>
        
        <v-textarea
          outlined
          name="input-7-4"
          label="Reason (min 100 words)"
          value=""
          required
          :rules="[$store.state.rules.required, $store.state.rules.textareaMin]"
          v-model="$store.state.ls.reason"
          counter
        ></v-textarea>

        <div class="btn-container">
            <v-btn
            depressed
            height="50"
            width="20%"
            class="fot-weight-bold white--text mr-2"
            color="#1976d2"
            @click="updatePreviousStep(orderStep)"
          >
            <v-icon medium left class="ml-1">fas fa-chevron-left</v-icon>
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
            <v-icon medium left class="ml-1">fas fa-chevron-right</v-icon>
          </v-btn>
        </div>
    </v-form>
</template>

<script>
import { mapGetters } from "vuex";
export default {
    name: 'OrderForm',
    props: ["orderstep"],
    computed: {
        ...mapGetters({
            // categories: "ls/getCategories",
        }),
        // updateStep: function(){
        //     this.orderstep = 2
        //     return this.orderstep 
        // }
    },
    data(){
        return{
            messageValue: "", // contact meg field model
            email: "", // contact email field model
            name: "", // contact name field model
            emailSended: false,
            contactFormErr: false,
        }
    },
    created(){},
    methods: {
        updateStep(stepNum){
            let self = this;
            let store = self.$store.state.ls;
            let formErrMsg = document.querySelector(".form-err-msg");
            let validationErrMsg = document.querySelector('.v-messages__message');
            if (store.what != null && store.category != null && store.reason != null) {
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
    .btn-container{
        width: 100%;
        height: auto;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
</style>