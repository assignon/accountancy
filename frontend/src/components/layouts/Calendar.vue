<template>
    <div class='calendar-core'>
        <v-date-picker
            ref="picker"
            v-model="date"
            full-width
            flat
            @click:date="emitEvents"
            color="#15141c"
            class='hidden-sm-and-down'
        ></v-date-picker>
        <v-dialog
            v-model="$store.state.mobileCalendarStatus"
            persistent
            max-width="600px"
            class='hidden-md-and-up'
            >
                <v-date-picker
                    ref="picker"
                    v-model="date"
                    full-width
                    flat
                    @click:date="emitEvents"
                    color="#15141c"
                ></v-date-picker>
        </v-dialog>
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
          this.$emit('transfer', date) // transfer products
          this.$emit('receive', date) // received products
          this.$emit('productWaiting', date) // added and updated product not validated by admin 
          setTimeout(() => {
              this.$store.state.mobileCalendarStatus=false
          }, 100)
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