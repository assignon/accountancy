// import axios from "axios";

export default {
    namespaced: true,

    state: {
        productsArr: [],
        addedProductsArr: [],
    },

    getters: {
        getProducts: (state) => {
            return state.productsArr
        },
        getAddedProducts: (state) => {
            return state.addedProductsArr
        }
    },

    mutations: {
    
    },

    actions: {
        
    },
  
}