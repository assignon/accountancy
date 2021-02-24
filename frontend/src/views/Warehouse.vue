<template>
    <div class="warehouse-core animated fadeIn">
        <h2 class='mb-5' style='margin-left:5%;'>The warehouses</h2>
        <v-layout 
            class='wh-temp-layout animated fadeInUp pt-3 pb-3 pl-5'
            v-for="(whouse,i) in warehouses[0]"
            :key='i'
        >
            <v-flex xs12 sm12 md5 lg5 xl5 class='warehouse-name' @click.stop='$store.state.infoDrawer=true, whouseDetails(whouse.id)'>
                <p><v-icon small color='#1e1d2b'>fas fa-warehouse</v-icon>
                    {{whouse.name}}<span v-if='whouse.su'>[main]</span>
                </p>
            </v-flex>

            <v-flex xs12 sm12 md3 lg3 xl3 class='date' @click.stop='$store.state.infoDrawer=true, whouseDetails(whouse.id)'>
                <p>
                    <v-icon small color='#1e1d2b' class='mr-1'>fas fa-calendar-alt</v-icon>
                    {{parseDate(whouse.added_on)}}
                </p>
            </v-flex>

            <v-flex xs12 sm12 md4 lg4 xl4 class='wh-actions' v-if='!whouse.su'>
                <v-icon medium color='#0163d1' class='mr-3' @click.stop='updateWh(whouse.id)'>fas fa-pencil-alt</v-icon>
                <v-icon medium color='#fc0e26' class='ml-3' @click.stop='deleteWh(whouse.id)'>fas fa-trash-alt</v-icon>
            </v-flex>

        </v-layout>
        <!-- imformation dialog -->
        <InformationModal 
            bColor='#15141c'    
            border='1px solid #15141c'
            closeClr='white' 
        />
    </div>
</template>

<script>
import InformationModal from "@/components/modals/InformationModal.vue";
import { mapGetters } from "vuex";
export default {
  name: "Warehouse",

  components: {
      InformationModal,
  },

  computed: {
    ...mapGetters({
        warehouses: 'dashboard/getWraehouse',
    }),
  },

  data(){
    return{

    }
  },

  created(){
    //   console.log(this.warehouses);
  },

  methods: {
    parseDate(date){
        return new Date(date).toDateString()
    },

    whouseDetails(whouseId){
        let self = this;

        self.$store.dispatch("getReq", {
            url: 'dashboard/get_user_data',
            params: {user_id: whouseId},
            auth: self.$session.get('token'),
            csrftoken: self.$session.get('token'),
            callback: function(data) {
                console.log(data);
                self.$store.getters["setData"]([self.$store.state.dashboard.whouseDetailsArr, [data]]);
                self.$store.state.infoTempName = 'WhouseDetails'
            },
        });
    },

    updateWh(whouseId){
        console.log(whouseId);
    },

    deleteWh(whouseId){
        console.log(whouseId);
    },
  }
};
</script>

<style scoped>
  .warehouse-core{
    height: auto;
    width: 85%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    margin-left: 15%;
    margin-top: 70px;
    background-color: #fafafa;
  }
  .wh-temp-layout{
        height: auto;
        width: 70%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
        border: 1px solid #ebf0f7;
        border-radius: 10px;
        background-color: #ebf0f7;
        padding: 5px;
        cursor: pointer;
        margin-bottom: 10px;
        margin-left: 5%;
        box-shadow: rgba(255, 255, 255, 0.2) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0.9) 0px 0px 0px 1px;
    }
    .warehouse-name{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .date p, .warehouse-name p{
        color: #1e1d2b;
        font-size: 15px;
        text-align: left;
        width: 100%;
        padding: 0px;
        margin: 0px;
        font-weight: bold;
        overflow: hidden;
    }
    .wh-actions{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: flex-end;
    }
    .wh-action .v-icon{
        cursor: pointer;
    }
  
</style>
