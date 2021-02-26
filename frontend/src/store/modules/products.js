// import axios from "axios";

export default {
    namespaced: true,

    state: {
        productsArr: [],
        addedProductsArr: [],
        BrandssArr: [],
        vehiclesArr: [],
        filteredProductsArr: [],
        productDetailsArr: [],
        addProductForm: true,
        transferDialog: false,
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
        },
        getProductDetails: (state) => {
            return state.productDetailsArr
        }
    },

    mutations: {
    
    },

    actions: {
        
    },
  
}