<template>
    <div class="whouse-detail-core animated fadeIn">
       
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
      console.log(this.whouseDetails);
  },

  methods: {
    
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
</style>
