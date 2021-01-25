<template>
    <div class='progress-bar-core'>
       <v-progress-linear
            color= "#0163d1"
            height="7"
            rounded
            class='ml-3 mt-3'
            :value="paymentProgressValue"
        >
            <!-- <small style=''>{{ Math.ceil(progress) }}%</small> -->
        </v-progress-linear> 
    </div>
</template>

<script>
export default {
    name: 'ProgressBar',

    props:['times', 'paymentDatesArr'],

    computed:{
        paymentProgressValue: function(){
            // let currentDate = new Date().toISOString().split('T')[0]
            // let parts = 100/this.times
            // let payment_turn = this.paymentDatesArr.indexOf(currentDate)
            console.log(this.paymentDatesArr);

            // return payment_turn*parts
            return 50
        }
    },

    data(){
        return{

        }
    },

    methods:{
    
    }
}
</script>

<style scoped>
    .progress-bar-core{
        width: 30%;
        height: auto;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>