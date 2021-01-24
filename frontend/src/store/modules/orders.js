// import axios from "axios";

export default {
    namespaced: true,
    state: {
        ordersArr: [],
        paymentsArr: [],
    },

    getters: {
        getOrders: (state) => {
            return state.ordersArr
        },
        getPayments: (state) => {
            return state.paymentsArr
        }
    },

    mutations: {
    
    },

    actions: {
        
    },
  
}