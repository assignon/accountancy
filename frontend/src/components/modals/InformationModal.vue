<template>
    <v-navigation-drawer
      v-model="$store.state.infoDrawer"
      fixed
      height='100vh'
      :width= 'dialogWidth'
      right
      :overlay='false'
      class='info-drawer'
      :style="{backgroundColor: bColor,border: border}"
    >   
        <div class='header ml-2' @click='$store.state.infoDrawer=false'>
            <v-icon medium :color="closeClr">fas fa-times</v-icon>
        </div>
        <component :is="$store.state.infoTempName"></component>
    </v-navigation-drawer>
</template>

<script>
import OrderDetails from "@/components/layouts/OrderDetails";
import ProductDetails from "@/components/layouts/ProductDetails";
import PaymentDetails from "@/components/layouts/PaymentDetails";
import WhouseDetails from "@/components/layouts/WhouseDetails";
export default {
    name: 'InformationModal',

    props: ['bColor', 'border', 'closeClr'],

    components: {
        PaymentDetails,
        ProductDetails,
        OrderDetails,
        WhouseDetails,
    },

    data(){
        return {
            // datailsTemplates: ['PaymentDetails', 'ProductDetails', 'OrderDetails']
            dialogWidth: window.innerWidth > 500 ? '50%' : '100%'
        }
    },

    created() {},

    methods: {}
}
</script>

<style scoped>
    /* .v-navigation-drawer--is-mobile:not(.v-navigation-drawer--close), .v-navigation-drawer--temporary:not(.v-navigation-drawer--close){
        box-shadow: none;
    } */
    .info-drawer{
        width: 50%;
    }
    .theme--light.v-navigation-drawer{
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .header{
        width: 90%;
        height: auto;
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
        padding: 10px;
        cursor: pointer;
    }
    .v-overlay{
        top:unset;
    }
    .report-form-drawer{
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .v-navigation-drawer__content{
        width:100%;
    }
     @media only screen and (max-width: 1500px) {
        .info-drawer{
            width: 80%;
        }
    }
    @media only screen and (max-width: 500px){
        .info-drawer{
            width: 100%;
        }
    }
</style>