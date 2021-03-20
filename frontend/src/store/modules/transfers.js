import axios from "axios";

export default {
    namespaced: true,
    state: {
        productReceivedArr: [],
        productTransferedArr: [],
        productTransferedDetailsArr: [],
        startDate: new Date().toISOString().substr(0, 10),
    },

    getters: {
        getReceivedProduct: (state) => {
            return state.productReceivedArr
        },
        getTransferedProduct: (state) => {
            return state.productTransferedArr
        },
        getTransferedProductDetails: (state) => {
            return state.productTransferedDetailsArr
        },
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