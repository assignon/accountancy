<template>
    <div class='transfer-core'>
        <v-layout class='transfer-layout'>
            <div class='transfer-head'>
                <v-btn
                    class="mr-4 hidden-sm-and-down"
                    large
                    color="#1976d2"
                    style='cursor:pointer'
                    rounded
                    @click='$store.state.calendarStatus = !$store.state.calendarStatus'
                >
                    <v-icon left style='font-size:20px;' class='pl-2 pt-2 pb-2' color='white'>
                        fas fa-calendar-alt
                    </v-icon>
                    <span v-if='$store.state.calendarStatus' style='color:white;'>Hide Calendar</span>
                    <span v-else style='color:white;'>Show Calendar</span>
                </v-btn>
            </div>

            <div class='transfer-body'>
                <v-card  flat  width='100%' class='transfer-flex'>
                    <v-tabs
                        v-model="tab"
                        background-color="white"
                        dark
                        slider-color='#15141c'
                    >
                        <v-tab class='ml-5'>
                            <p style='color:#15141c;font-size: 17px;text-transform:capitalize;font-weight:bold'>
                                <v-icon style='font-size: 30px;' color='#15141c'>fas fa-share-square</v-icon>
                                Transfered ({{productTransfered[0].count}})
                            </p>
                        </v-tab>
                        <v-tab class='ml-5'>
                            <p style='color:#15141c;font-size: 17px;text-transform:capitalize;font-weight:bold'>
                                <v-icon  style='font-size: 30px;' color='#15141c'>fas fa-reply</v-icon>
                                Received ({{productReceived[0].count}})
                            </p>
                        </v-tab>

                        <v-tabs-items v-model='tab' class='mt-5'>
                            <v-tab-item v-if='productTransfered.length > 0'>
                                <div
                                    class='transfer-temp animated fadeInUp pt-5 pb-5 ml-5'
                                    v-for="(transfer,i) in productTransfered[0].transfers"
                                    :key='i'
                                >
                                    <v-flex xs11 sm11 md4 lg4 xl4 class='transfer-flex ml-5'><strong>{{transfer.size}}</strong></v-flex>
                                    <v-flex xs11 sm11 md4 lg4 xl4 class='transfer-flex'>from: <strong>{{transfer.sender_name}}</strong></v-flex>
                                    <v-flex xs11 sm11 md4 lg4 xl4 class='transfer-flex'>to: <strong>{{transfer.receiver}}</strong></v-flex>
                                    <v-flex xs11 sm11 md4 lg4 xl4 class='transfer-flex'>quantity: <strong>{{transfer.quantity}}</strong></v-flex>
                                    <v-flex xs11 sm11 md4 lg4 xl4 class='transfer-flex' v-if='transfer.status=="pending"'><strong style='color:orange'> {{transfer.status}}</strong></v-flex>
                                    <v-flex xs11 sm11 md4 lg4 xl4 class='transfer-flex' v-if='transfer.status=="accept"'><strong style='color:green'> {{transfer.status}}ed</strong></v-flex>
                                    <v-flex xs11 sm11 md4 lg4 xl4 class='transfer-flex' v-if='transfer.status=="reject"'><strong style='color:red'> {{transfer.status}}ed</strong></v-flex>
                                </div>
                            </v-tab-item>
                            <v-tab-item v-else>
                                <div class='no-transfer' style='margin-top:50px;'>
                                    <v-icon>fas fa-share-square</v-icon>
                                    <p class='mt-3'>No Transfer</p>
                                </div>
                            </v-tab-item>

                            <v-tab-item v-if='productReceived.length > 0'>
                                <div
                                    class='transfer-temp animated fadeInUp pt-5 pb-5 ml-5'
                                    v-for="(receive,i) in productReceived[0].receives"
                                    :key='i'
                                >
                                    <v-flex xs11 sm11 md4 lg4 xl4 class='transfer-flex ml-5'><strong>{{receive.size}}</strong></v-flex>
                                    <v-flex xs11 sm11 md4 lg4 xl4 class='transfer-flex'>from: <strong>{{receive.sender_name}}</strong></v-flex>
                                    <v-flex xs11 sm11 md4 lg4 xl4 class='transfer-flex'>quantity: <strong>{{receive.quantity}}</strong></v-flex>

                                    <v-flex xs11 sm11 md4 lg4 xl4 class='btn-container mr-5' v-if='receive.status=="pending"'>
                                        <v-btn medium color='green' class='mr-5' @click='updateTransferStatus("accept", receive.id)'><span style='color:white'>Accept</span></v-btn>
                                        <v-btn medium color='red' class='ml-5' @click='updateTransferStatus("reject", receive.id)'><span style='color:white'>Reject</span></v-btn>
                                    </v-flex>
                                    <v-flex xs11 sm11 md4 lg4 xl4 v-else><strong>{{receive.status}}ed</strong></v-flex>
                                </div>
                            </v-tab-item>
                            <v-tab-item v-else>
                                <div class='no-transfer' style='margin-top:50px;'>
                                    <v-icon>fas fa-reply</v-icon>
                                    <p class='mt-3'>No Product Received</p>
                                </div>
                            </v-tab-item>
                        </v-tabs-items>
                    </v-tabs>
                </v-card>
                <!-- calendar -->
                <v-flex xs12 sm12 md4 lg4 xl4 class='calendar-flex mt-5 mr-5' v-if='$store.state.calendarStatus'>
                    <Calendar 
                        @transfer='getTransfers'
                        @receive='getReceives'
                    />
                </v-flex>
            </div>
        </v-layout>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import Calendar from "@/components/layouts/Calendar.vue";
export default {
    name: 'Transfers',

    components: {
        Calendar,
    },

    computed: {
        ...mapGetters({
            productReceived: 'transfers/getReceivedProduct',
            productTransfered: 'transfers/getTransferedProduct',
            productTransferedDetails: 'transfers/getTransferedProductDetails',
        }),
    },

    data(){
        return {
            tab: null,
        }
    },

    created(){
        this.getTransfers(null)
        this.getReceives(null)
        console.log(this.productTransfered[0].transfers);
    },

    methods: {
        getTransfers(date){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/product_transfered",
                params: {
                    wh_id: this.$session.get('warehouseId'),
                    sender_id: this.$session.get('userId'),
                    date: date,
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log('payments',data);
                    store.getters["setData"]([store.state.transfers.productTransferedArr, [data]]);
                },
            });
        },

        getReceives(date){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/product_received",
                params: {
                    wh_id: this.$session.get('warehouseId'),
                    receiver_name: self.$session.get('warehouseName'),
                    date: date,
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log('payments',data);
                    store.getters["setData"]([store.state.transfers.productReceivedArr, [data]]);
                },
            });
        },

        transferDetails(id){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/transfer_details",
                params: {
                    id: id,
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log('payments',data);
                    store.getters["setData"]([store.state.transfers.productTransferedDetailsArr, [data]]);
                },
            });
        },

        updateTransferStatus(status, transferId){
            let self = this;
            // let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "product/update_transfer_status",
                params: {
                    transfer_id: transferId,
                    status: status,
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log('payments',data);
                    if(data.updated){
                        self.getReceives(null)
                    }
                },
            });
        }
    }
}
</script>

<style scoped>
    .transfer-core{
        height: auto;
        width: 85%;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        margin-left: 15%;
        /* background-color: #1e1d2b; */
        background-color: #ffffff;
    }
    .transfer-layout{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: flex-start;
        padding-top: 30px;
    }
    .transfer-head{
        width: 100%;
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
    }
    .transfer-head .v-btn{
        color: #fff;
        font-size: 15px;
        font-weight: bolder;
        text-transform: capitalize;
    }
    .transfer-body{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: flex-start;
        padding-top: 30px;
    }
    .transfer-flex{
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 90%;
    }
    /* .v-window__container{
        width: 100%;
    }
    .v-tabs {
        width: 100%;
        height: auto;
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        border: 1px green; 
    }
    .v-tabs-items{
        width: 100%;
        height: auto;
        min-height: 80vh;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    } */
    .no-transfer{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height:80vh;
    }
    .no-transfer .v-icon{
        font-size: 100px;
        color: #1e1d2b;
    }
    .no-transfer p{
        text-align: center;
        color: #1e1d2b;
        font-size: 20px;
        font-weight: bold;
    }
    .calendar-flex{
        height: auto;
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
    }
    .transfer-temp{
        height: auto;
        width: 90%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
        border: 1px solid #ebf0f7;
        border-radius: 10px;
        background-color: #ebf0f7;
        padding: 5px;
        cursor: pointer;
        margin-bottom: 20px;
        margin-top: 20px;
        box-shadow: rgba(255, 255, 255, 0.2) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0.9) 0px 0px 0px 1px;
    }
    .transfer-temp .transfer-flex{
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .btn-container{
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }
      @media only screen and (max-width: 500px) {
        .transfer-core{
            width: 100%;
            align-items: center;
            margin-left: 0%;
        }
    }
 </style>

