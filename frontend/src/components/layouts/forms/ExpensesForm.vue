<template>
    <v-form class='expenses-form' ref='expensesForm'>
        <p class="mb-4 font-weight-bold">Add New expense</p>
        <v-spacer></v-spacer>
        <p class='expenses-err mb-4'></p>
        <v-text-field
            label='Expense Name'
            required
            outlined
            :rules="[$store.state.rules.required]"
            v-model='$store.state.expenses.name'
        ></v-text-field>
            <v-text-field
            label='Expense Price'
            required
            outlined
            :rules="[$store.state.rules.required]"
            v-model='$store.state.expenses.price'
            type='number'
        ></v-text-field>
        <v-spacer></v-spacer>
        <div class='btn-container'>
            <v-btn
                color="blue darken-1"
                text
                @click="$store.state.expenses.expensesDialog = false"
            >
                Close
            </v-btn>
            <v-btn
            depressed
                height="50"
                width="20%"
                class="fot-weight-bold white--text"
                color="#1976d2"
                v-if='$store.state.product.addProductForm'
                @click="addExpense()"
            >
                <p style='font-size:17px;margin:auto;'>Add</p>
            </v-btn>
        </div>
    </v-form>
</template>

<script>
export default {
    name: 'ExpensesForm',

    data(){
        return{

        }
    },

    created(){},

    methods: {
        addExpense(){

        }
    }
}
</script>

<style scoped>
    .expenses-form{
        width: 100%;
        height: auto;
        min-height: 94%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        background-color: #fffafa;
        padding: 50px;
    }
    .product-field-container{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .expenses-form .v-text-field{
         width: 100%;
     }
    .expenses-err{
        width: 100%;
        height: auto;
        text-align: left;
        color: #15141c;
        font-size: 15px;
    }
   
    .btn-container{
        width: 100%;
        height: auto;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    .v-btn{
        text-transform: capitalize;
    }
</style>