<template>
    <div>
       <v-progress-linear
            :color= "currentProgress[i]['progress_clr']"
            height="7"
            class='ml-3 mt-3'
            :value="(currentProgress[i][ls.fields.what]*100)/totalProgress[i][ls.fields.what]"
        >
            <!-- <small style=''>{{ Math.ceil(progress) }}%</small> -->
        </v-progress-linear> 
    </div>
</template>

<script>
export default {
    name: 'ProgressBar',

    props:[],

    data(){
        return{

        }
    },

    methods:{
        
    }
}
</script>