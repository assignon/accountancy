<template>
    <v-form class="order-form animated" ref="orderForm">
        <p class='quality-form-err-msg'></p>

        <v-stepper
            v-model="orderFormStep"
            vertical
            class='order-stepper'
        >   <!-- customer information -->
            <v-stepper-step
                :complete="orderFormStep > 1"
                step="1"
            >
                Customer Informtions
                <small>Summarize if needed</small>
            </v-stepper-step>

            <v-stepper-content step="1">
               <LsBase :orderFormStep="orderFormStep" @updatestep='orderFormStep = 2' />
            </v-stepper-content>
            <!-- order -->
            <v-stepper-step
                :complete="orderFormStep > 2"
                step="2"
            >
                Order
                <small>Summarize if needed</small>
            </v-stepper-step>

            <v-stepper-content step="2">
               <LsTime :orderFormStep="orderFormStep" @updateprevstep='orderFormStep = 1' @updatestep='orderFormStep = 3' />
            </v-stepper-content>
            <!-- payment details -->
            <v-stepper-step
                :complete="orderFormStep > 3"
                step="3"
            >
                Payment Informtions
                <small>Summarize if needed</small>
            </v-stepper-step>

            <v-stepper-content step="3">
               <LsQuality :orderFormStep="orderFormStep" @updateprevstep='orderFormStep = 2' @submit='createLs()' />
            </v-stepper-content>
        </v-stepper>
    </v-form>
</template>

<script>
export default {
    name: 'OrderForm',
    
    props: [],

    computed: {},

    data(){
        return{
            orderFormStep: 1
        }
    },
    created(){},
    methods: {
        submitLs(){
        //     let self = this;
        //     let store = self.$store.state.ls;
        //     let formErrMsg = document.querySelector(".quality-form-err-msg");
        //     let validationErrMsg = document.querySelector('.v-messages__message');
            
        //     if (self.$store.state.ls.qualitycriteriaArr.length >= 3 && store.dod != null) {
        //         if(!document.body.contains(validationErrMsg)){
        //             self.$emit('submit')
        //         }else{
        //             formErrMsg.innerHTML = validationErrMsg.textContent;
        //         }
        //     } else {
        //         formErrMsg.innerHTML = "Definition Of Done field is empty or quality criteria < 7";
        //     }
        },
    },
}
</script>

<style scoped>
    .order-form{
        width: 100%;
        height: 90%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: white;
    }
    .qualities{
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
        margin-bottom: 10px;
    }
    .add-categories{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-end;
        margin-bottom: 20px;
        margin-top: 20px;
    }
     .add-categories .v-text-field{
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