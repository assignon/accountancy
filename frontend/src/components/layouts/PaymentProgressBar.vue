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
            let currentDate = new Date().toISOString().split('T')[0]
            let parts = 100/this.times
            let dateIndexArr = []

            this.paymentDatesArr.forEach(date => {
                if (currentDate > date){
                    dateIndexArr = []
                    dateIndexArr.push(this.paymentDatesArr.indexOf(date)+1)
                }
            })

            return dateIndexArr[0]*parts
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