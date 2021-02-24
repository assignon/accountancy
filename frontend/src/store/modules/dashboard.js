// import axios from "axios";

export default {
    namespaced: true,

    state: {
        warehouseDialog: false,
        warehouseName: null,
        email: null,
        upassword: null,
        rPassword: null,
        formActionType: 'add', //check if user wanna add or update
        warehouseId: null,
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