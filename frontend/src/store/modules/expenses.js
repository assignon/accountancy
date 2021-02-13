// import axios from "axios";

export default {
    namespaced: true,

    state: {
        name: null,
        price: null,
        expensesDialog: false,
        expensesArr: [],
    },

    getters: {
        getExpenses: (state) => {
            return state.expensesArr
        },
        
    },

    mutations: {
    
    },

    actions: {}

}