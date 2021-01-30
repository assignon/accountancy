// import axios from "axios";

export default {
    namespaced: true,

    state: {
        productsArr: [],
        addedProductsArr: [],
        BrandssArr: [],
        filteredProductsArr: [],
    },

    getters: {
        getProducts: (state) => {
            return state.productsArr
        },
        getAddedProducts: (state) => {
            return state.addedProductsArr
        },
        getBrandss: (state) => {
            return state.BrandssArr
        },
        getProfiles: (state) => {
            return state.filteredProductsArr
        }
    },

    mutations: {
    
    },

    actions: {
        
    },
  
}