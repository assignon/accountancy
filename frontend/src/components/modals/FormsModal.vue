<template>
   <v-dialog
        v-model="$store.state.formsDialog"
        fullscreen
        hide-overlay
        transition="dialog-bottom-transition"
        class='stepper-dialog'
    >
        <v-toolbar
            dark
            color="#15141c"
        >
            <h3 style='color: #fff'>New {{$store.state.formName}}.</h3>
            <v-spacer></v-spacer>
            <v-btn
                icon
                dark
                @click="$store.state.formsDialog = false, reloadPage()"
            >
                <v-icon color='white'>mdi-close</v-icon>
            </v-btn>
            <!-- <v-toolbar-items>
                <v-btn
                dark
                text
                @click="dialog = false"
                >
                Save
                </v-btn>
            </v-toolbar-items> -->
        </v-toolbar>
        <component :is="$store.state.formsTemp"></component>
    </v-dialog>
</template>

<script>
import OrderStepper from "@/components/layouts/forms/OrderStepper.vue";
import ProductForm from "@/components/layouts/forms/ProductForm.vue";
import { mapGetters } from 'vuex';
export default {
  name: "Order",

  props: [],
  
    components: {
        OrderStepper,
        ProductForm,
    },

    computed: {
        ...mapGetters({
        }),
    },


  data(){
    return{
      
    }
  },

  created(){
  },

  methods: {
    reloadPage(){
        if(this.$store.reload){
            window.location.reload()
        }
    }
  }
};
</script>

<style scoped>
.stepper-dialog{
    height: 90%;
}
::-webkit-scrollbar {
  width: 0px;
}
  /* .v-dialog, .v-dialog--fullscreen{
      background-color: #1e1d2b;
  } */
</style>
