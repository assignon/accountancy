<template>
    <div class='calendar-core'>
        <v-date-picker
        ref="picker"
        v-model="date"
        full-width
        flat
        @click:date="emitEvents"
        color="#15141c"
      ></v-date-picker>
    </div>
</template>

<script>
export default {
    name: 'Calendar',

    data(){
        return{
            date: new Date().toISOString().substr(0, 10),
            pickerDate: null,
            events: [],
            colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
        }
    },

    watch: {
    //   pickerDate (val) {
    //       console.log(val);
    //     this.notes = [
    //       this.allNotes[Math.floor(Math.random() * 5)],
    //       this.allNotes[Math.floor(Math.random() * 5)],
    //       this.allNotes[Math.floor(Math.random() * 5)],
    //     ].filter((value, index, self) => self.indexOf(value) === index)
    // },
    },

    mounted () {
    //   this.$refs.calendar.checkChange()
    },

    created(){
        
    },

    methods: {
      emitEvents(date){
          this.$emit('orders', date)
          this.$emit('payments', date)
          this.$emit('addedProducts', date)
          this.$emit('expenses', date)
      }
    },
}
</script>

<style scoped>
    .calendar-core{
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
</style>