<template>
    <v-form class='expenses-form' ref='expensesForm'>
        <p class="mb-4 font-weight-bold">
            Add New expense to 
            <span style='color: #0163d1;font-weight:bold' v-if='Number($session.get("warehouseId"))==$session.get("userId") || $session.get("warehouseName")=="all"'>Main</span>
            <span style='color: #0163d1;font-weight:bold' v-else>{{$session.get('warehouseName')}}</span>
            warehouse
        </p>
        <v-spacer></v-spacer>
        <p class='expenses-err mb-4'></p>
        <v-text-field
            label='Expense*'
            required
            outlined
            :rules="[$store.state.rules.required]"
            v-model='$store.state.expenses.name'
        ></v-text-field>
            <v-text-field
            label='Amount*'
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
            let self = this;
            let body = {
                name: self.$store.state.expenses.name,
                price: self.$store.state.expenses.price,
                user_id: this.$session.get('warehouseId') == '0' ? this.$session.get('userId') : this.$session.get('warehouseId')
            }
            let formErrMsg = document.querySelector(".expenses-err");
            let validationErrMsg = document.querySelector('.v-messages__message');

            if(body.name != null && body.price != null && body.price >= 0 && !document.body.contains(validationErrMsg)){
                self.$store.dispatch("postReq", {
                    url: "expense/new_expense",
                    params: body,
                    auth: self.$session.get('token'),
                    csrftoken: self.$session.get('token'),
                    callback: function(data) {
                        console.log(data);
                        if(data.added){
                            formErrMsg.innerHTML = 'Expense added'
                            document.querySelector('.expenses-form').reset()
                            //close dialog after 2sec
                            setTimeout(() => {self.$store.state.expenses.expensesDialog = false, formErrMsg.innerHTML = '', window.location.reload()}, 2000)
                        }else{
                            formErrMsg.innerHTML = 'Something went wrong'
                        }
                    },
                });
            }else{
                formErrMsg.innerHTML = 'Enter the expense name and price'
            }
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