<template>
    <v-dialog
         v-model="$store.state.order.printDialog"
        fullscreen
        hide-overlay
        transition="dialog-bottom-transition"
        class='print-sales-core'
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
                @click="$store.state.order.printDialog = false"
            >
                <v-icon color='white'>mdi-close</v-icon>
            </v-btn>
        </v-toolbar>
        <v-layout class='print-sale-layout'>
            <v-form class='print-dialog-form'>
                <!-- start date picker -->
                <v-menu
                    v-model="menuStart"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    transition="scale-transition"
                    offset-y
                    min-width="290px"
                    class='start-date'
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                            v-model="startDate"
                            label="From"
                            prepend-icon="mdi-calendar"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                            required
                            outlined
                        ></v-text-field>
                    </template>
                    <v-date-picker
                        v-model="startDate"
                        @input="menuStart = false"
                    ></v-date-picker>
                </v-menu>
                <!-- end date picker -->
                <v-menu
                    v-model="menuEnd"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    transition="scale-transition"
                    offset-y
                    min-width="290px"
                    class='start-date ml-5'
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                            v-model="endDate"
                            label="To"
                            prepend-icon="mdi-calendar"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                            required
                            outlined
                        ></v-text-field>
                    </template>
                    <v-date-picker
                        v-model="endDate"
                        @input="menuEnd = false"
                    ></v-date-picker>
                </v-menu>
                
                <div class='btn-container'>
                    <v-btn
                    depressed
                        height="50"
                        width="20%"
                        class="fot-weight-bold white--text"
                        color="#1976d2"
                        @click="printSales()"
                    >
                        <p style='font-size:17px;margin:auto;'>Print</p>
                    </v-btn>
                </div>
            </v-form>
            <!-- sales container -->
            <div class='sales-content'>
                <PrintSalesContent :data='printOrders[0]' />
            </div>
        </v-layout>
    </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex';
import PrintSalesContent from "@/components/layouts/PrintSalesContent.vue";
export default {
    name: 'printSales',

    components: {
        PrintSalesContent
    },

    data() {
        return {
            printDialog: false,
             // date picker
            menuStart: false,
            menuEnd: false,
            startDate: new Date().toISOString().substr(0, 10),
            endDate: new Date().toISOString().substr(0, 10),
        }
    },

     computed: {
        ...mapGetters({
            printOrders: 'order/getPrintSales',
        }),
    },

    created() {
        
    },

    methods: {
        compareDate(date1, date2){
            let result = {};
            let startDate = new Date(date1);
            let endDate = new Date(date2);
            if(startDate > endDate){
                result = {pass: false, msg: 'The end date shoul be in the future'}
            }else if(+startDate === +endDate){
                result = {pass: false, msg: 'The end date should not be the same as the start date'}
            }
            else if(startDate.toDateString() == new Date().toDateString()){
                result = {pass: true, msg: ''}
            }
            // else if(new Date().toISOString() > startDate.toISOString()){
            //     result = {pass: false, msg: 'The start date cannot be in the past'}
            // }
            else{
                result = {pass: true, msg: ''}
            }
            return result;
        },

        printSales(){
            let self = this;
            let store = self.$store

            if (self.startDate != null && self.endDate != null) {
                if(self.compareDate(self.startDate, self.endDate).pass){
                    this.$store.dispatch("getReq", {
                        url: "order/print_order",
                        params: {
                            start: self.startDate,
                            end: self.endDate,
                            user_id: this.$session.get('warehouseId'),
                        },
                        auth: self.$session.get('token'),
                        csrftoken: self.$session.get('token'),
                        callback: function(data) {
                            console.log('print order',data);
                            store.getters["setData"]([store.state.order.printSalesArr, [data]]);
                            console.log(self.printOrders);
                        },
                    });
                }else{
                    alert(self.compareDate(self.startDate, self.endDate).msg);
                }
            }
        }
    }
}
</script>

<style scoped>
    .print-sales-core{
        height: 90vh;
    }
    ::-webkit-scrollbar {
    width: 0px;
    }
    .print-sale-layout{
        width: 100%;
        height: 95%;
        padding: 30px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        background-color: white;
        overflow: scroll;
    }
    .print-dialog-form{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .print-dialog-form .v-text-field{
        width: 100%;
    }
    .btn-container{
        width: 40%;
        height: auto;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        margin-left: 10px;
    }
    .v-btn{
        text-transform: capitalize;
    }
    .sales-content{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
</style>