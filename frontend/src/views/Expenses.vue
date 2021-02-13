<template>
    <div class='expenses-core'>
        <v-layout class='expenses-layout'>
            <v-flex xs12 sm12 md8 lg9 xl9 class='expenses-flex'>
                <div class='expenses-container' v-if='expenses[0].count > 0'>
                    <!-- <div 
                        class='expenses-temp-layout animated fadeInUp'
                        v-for="(expense,i) in expenses[0].expenses"
                        :key='i'
                    >
                        <v-flex xs12 sm12 md4 lg4 xl4 class='expense-name'>
                            <p>{{order.credentials.name}}</p>
                        </v-flex>

                        <v-flex xs12 sm12 md4 lg3 xl3 class='date'>
                            <p>
                                <v-icon small color='#1e1d2b' class='mr-1'>fas fa-calendar-alt</v-icon>
                                {{parseDate(order.order.order_on)}}
                            </p>
                        </v-flex>

                        <v-flex xs12 sm12 md3 lg3 xl3 class='price'>
                            <p>
                                <v-icon small color='#1e1d2b' class='mr-1'>fas fa-coins</v-icon>
                                {{formatPrice(order.paying)}}FRS
                            </p>
                        </v-flex>

                        <v-flex xs12 sm12 md2 lg2 xl2 class='actions'>
                           <v-icon medium color='red'>fas fa-trash-alt</v-icon>
                        </v-flex>

                    </div> -->
                </div>

                <div class='no-expenses' v-else>
                    <v-icon color='#15141c' style='font-size: 100px'>fas fa-wallet</v-icon>
                    <p class='mt-3 font-weight-bold' style='font-size: 17px'>No Expenses</p>
                </div>
            </v-flex>

            <v-flex xs12 sm12 md4 lg3 xl3 class='calendar-flex mr-5'>
                <div class='calendar-container'>
                    <Calendar 
                        @expenses='getExpenses'
                    />
                </div>
                <div class='daily-total-expense'>
                    <div class='total-expense-head'>
                        <p><v-icon medium color='#15141c' class='mr-2'>fas fa-wallet</v-icon>Total Expenses</p>
                    </div>
                    <div class='total-expense'>
                        <h1>{{formatPrice(expenses[0].daily_total)}}FRS</h1>
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
                url: "expense/daily_expenses",
                params: {
                    date: date,
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
    .expenses-core{
        height: 100vh;
        width: 85%;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        margin-left: 15%;
        background-color: #ffffff;
        overflow-y: hidden;
    }
    ::-webkit-scrollbar {
        width: 0px;
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
        justify-content: center;
        align-items: center;
    }
    .expenses-container{

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
        box-shadow: rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;
    }
    .daily-total-expense{
        width: 100%;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
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
    }
    .total-expense h1{
        font-size: 40px;
        color: #15141c;
        width: 100%;
        height: auto;
    }
</style>