<template>
    <div class='expenses-core'>
        <div class='claendar-ctrl mt-5 hidden-sm-and-down' style='display:flex;justify-content:flex-end;align-items:center;width:97%;'>
            <v-btn
                class="font-weight-bold"
                large
                color="#1976d2"
                style='cursor:pointer;text-transform:capitalize'
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
        <v-layout class='expenses-layout'>
            <v-flex xs12 sm12 md8 lg9 xl9 class='expenses-flex'>
                <div class='expenses-container' v-if='expenses[0].count > 0'>
                    <div 
                        class='expenses-temp-layout animated fadeInUp mt-2 pt-3 pb-3'
                        v-for="(expense,i) in expenses[0].expenses"
                        :key='i'
                    >
                        <v-flex xs12 sm12 md4 lg4 xl4 class='expense-name'>
                            <p style='text-transform: capitalize'>{{expense.name}}</p>
                        </v-flex>

                        <v-flex xs12 sm12 md4 lg3 xl3 class='date'>
                            <p>
                                <v-icon small color='#1e1d2b' class='mr-1 hidden-sm-and-down'>fas fa-calendar-alt</v-icon>
                                {{parseDate(expense.add_on)}}
                            </p>
                        </v-flex>

                        <v-flex xs12 sm12 md3 lg3 xl3 class='price'>
                            <p>
                                <v-icon small color='#1e1d2b' class='mr-1 hidden-sm-and-down'>fas fa-coins</v-icon>
                                {{formatPrice(expense.price)}}FRS
                            </p>
                        </v-flex>

                        <!-- <v-flex xs12 sm12 md2 lg2 xl2 class='actions'>
                           <v-icon medium color='red'>fas fa-trash-alt</v-icon>
                        </v-flex> -->

                    </div>
                </div>

                <div class='no-expenses' v-else>
                    <v-icon color='#15141c' style='font-size: 100px'>fas fa-wallet</v-icon>
                    <p class='mt-3 font-weight-bold' style='font-size: 17px'>No Expenses</p>
                </div>
            </v-flex>

            <v-flex xs12 sm12 md4 lg3 xl3 class='calendar-flex mr-5'>
                <div class='calendar-container' v-if='$store.state.calendarStatus'>
                    <Calendar 
                        @expenses='getExpenses'
                    />
                </div>
                <div class='daily-total-expense'>
                    <div class='total-expense-head'>
                        <p><v-icon medium color='#15141c' class='mr-2'>fas fa-wallet</v-icon>Total Expenses</p>
                    </div>
                    <div class='total-expense'>
                        <h1 class='animated bounceIn'>Daily: {{formatPrice(expenses[0].daily_total)}}FRS</h1>
                        <h1 class='animated bounceIn'>Monthly: {{formatPrice(expenses[0].montly_total)}}FRS</h1>
                    </div>
                </div>
            </v-flex>
        </v-layout>
    </div>
</template>

<script>
import Calendar from "@/components/layouts/Calendar.vue";
import { mapGetters } from 'vuex';
export default {
    name: 'Expenses',

    components: {
        Calendar,
    },

    computed: {
        ...mapGetters({
            expenses: 'expenses/getExpenses',
        }),
    },

    data(){
        return{

        }
    },

    created(){
        this.getExpenses(null)
    },

    methods: {
        parseDate(date){
            return new Date(date).toDateString()
        },

        formatPrice(value) {
            let val = (value/1).toFixed(0).replace('.', ',')
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
        },

        getExpenses(date){
            let self = this;
            let store = self.$store;

            this.$store.dispatch("getReq", {
                url: "expense/expenses",
                params: {
                    date: date,
                    user_id: this.$session.get('warehouseId')
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log(data);
                    store.getters["setData"]([store.state.expenses.expensesArr, [data]]);
                },
            });
        }
    }
}
</script>

<style scoped>
::-webkit-scrollbar {
        width: 0px;
    }
    .expenses-core{
        height: 100vh;
        width: 85%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        margin-left: 15%;
        background-color: #ffffff;
        overflow-y: hidden;
    }
    .expenses-layout{
        height: 100%;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: flex-start;
        padding-top: 30px;
    }
    .expenses-flex{
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
    .expenses-container{
        height: 90%;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        overflow-y: scroll;
        overflow-x: hidden;
    }
    .expenses-temp-layout{
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
        margin-left: 5%;
        box-shadow: rgba(255, 255, 255, 0.2) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0.9) 0px 0px 0px 1px;
    }
    .date p, .expense-name p, .price p{
        color: #1e1d2b;
        font-size: 15px;
        text-align: center;
        width: 100%;
        padding: 0px;
        margin: 0px;
        font-weight: bold;
        overflow: hidden;
    }
    .actions .v-icon{
        cursor: pointer;
    }
    .no-expenses{
        height: 100%;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .calendar-flex{
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .calendar-container{
        height: auto;
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        border-radius: 5px;
        box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
    }
    .daily-total-expense{
        width: 100%;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        border-radius: 5px;
        box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
        margin-top: 30px;
    }
    .total-expense-head{
        width: 90%;
        height: 10%;
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        margin-left: 10%;
        margin-top: 30px;
    }
    .total-expense{
        width: 100%;
        height: 90%;
        display: flex;
        justify-content: center;
        align-items: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start
    }
    .total-expense h1{
        font-size: 25px;
        color: #15141c;
        width: 100%;
        height: auto;
    }
    @media only screen and (max-width: 500px){
        .expenses-core{
            width: 100%;
            align-items: center;
            margin-left: 0%;
        }
        .expenses-layout{
            flex-direction: column-reverse;
            justify-content: center;
        }
        .calendar-flex{
            align-items: center;
            width: 100%;
        }
        .expenses-flex{
            width: 100%;
        }
    }
</style>