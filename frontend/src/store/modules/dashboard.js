// import axios from "axios";

export default {
    namespaced: true,

    state: {
        userDataArr: [],
        warehouseArr: [],
        whouseDetailsArr: [],
    },

    getters: {
        getUserData(state) {
            return state.userDataArr
        },
        getWraehouse(state) {
            return state.warehouseArr
        },
        getWhouseDetails(state) {
            return state.whouseDetailsArr
        }
    },

    mutations: {
    
    },

    actions: {
        
    },
  
}