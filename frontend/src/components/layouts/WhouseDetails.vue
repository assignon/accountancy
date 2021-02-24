<template>
    <div class="whouse-detail-core animated fadeIn mt-5">
        <p>Warehouse name: {{whouseDetails[0].name}}</p>
        <p>Email: {{whouseDetails[0].email}}</p>
        <p>Administrator: {{boolToText(whouseDetails[0].admin)}}</p>
        <p>Staff: {{boolToText(whouseDetails[0].staff)}}</p>
        <p>Active: {{boolToText(whouseDetails[0].active)}}</p>
        <p>Added on: {{parseDate(whouseDetails[0].added_on)}}</p>
    </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "WarehouseDetails",

  components: {
  },

  computed: {
    ...mapGetters({
        whouseDetails: 'dashboard/getWhouseDetails',
    }),
  },

  data(){
    return{

    }
  },

  created(){
      console.log(this.whouseDetails[0].active);
  },

  methods: {
    parseDate(date){
        return new Date(date).toDateString()
    },

    boolToText(bool){
        if(bool) return 'Yes'
        return 'No'
    }
  }
};
</script>

<style scoped>
  .whouse-detail-core{
    height: 90vh;
    width: 500px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    margin-left: 15%;
  }
  .whouse-detail-core p{
      font-size: 17px;
      text-align: left;
      color: #fff;
      /* margin: 0px;
      padding: 0px; */
  }
</style>
