import axios from "axios";

export default {
    namespaced: true,
    state: {
        ordersArr: [],
        paymentsArr: [],
        customerOrderArr: [],
        customerPaymentArr: [],
        paymentMethodsArr: [],
        // customer informations
        email: null,
        name: null,
        address: null,
        telNumber: null,
        times: 2,
        startDate: new Date().toISOString().substr(0, 10),
        // order informations
        product: null,
        productArr: [],
        quantity: 1,
        vehicule: null,
        brands: [],
        profiles: [],
        // payment informations
        payInterval: null,
        payIn: null,
        payMethod: null,
        // payment status obj
        currentStatus: null, //payment status of the current date
    },

    getters: {
        getOrders: (state) => {
            return state.ordersArr
        },
        getPayments: (state) => {
            return state.paymentsArr
        },
        getCustomerOrder: (state) => {
            return state.customerOrderArr
        },
        getcustomerPayment: (state) => {
            return state.customerPaymentArr
        },
        getPaymentMethods: (state) => {
            return state.paymentMethodsArr
        }
    },

    mutations: {
        getAxiosCall(state, payload) {
        /*
                        http get request
                        params:
                            payload: [object]: [data sended with the request]
                    */
        axios
            .get(`${payload.host}/api/${payload.url}/`, {
            params: payload.params,
            headers: {
                "X-CSRFToken": payload.csrftoken,
                Authorization: `token ${payload.auth}`,
            },
            })
            .then(response => {
            let res = response.data;
            payload.callback(res);
            })
            .catch(error => {
            console.log(error);
            });
        },
    },

    actions: {
        getOrderDetails({ commit, rootState }, payload) {
            commit("getAxiosCall", {
                url: payload.url,
                params: payload.params,
                auth: payload.auth,
                csrftoken: payload.csrftoken,
                callback: payload.callback,
                host: rootState.HOST,
            });
        },
        getPaymentDetails({ commit, rootState }, payload) {
            commit("getAxiosCall", {
                url: payload.url,
                params: payload.params,
                auth: payload.auth,
                csrftoken: payload.csrftoken,
                callback: payload.callback,
                host: rootState.HOST,
            });
        },
    },
  
}