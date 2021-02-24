import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";
import Dashboard from "../views/Dashboard.vue";
import Warehouse from "../views/Warehouse.vue";
import Order from "../views/Order.vue";
import Product from "../views/Product.vue";
import Settings from "../views/Settings.vue";
import Expenses from "../views/Expenses.vue";
// import NotAuthorize from "../views/dashboard/NotAuthorize.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard
  },
  {
    path: "/warehouses",
    name: "Warehouse",
    component: Warehouse
  },
  {
    path: "/orders",
    name: "Order",
    component: Order
  },
  {
    path: "/products",
    name: "Product",
    component: Product
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings
  },
  {
    path: "/expenses",
    name: "Expenses",
    component: Expenses
  },
  // {
  //   path: "/notAuthorize",
  //   name: "NotAuthorize",
  //   component: NotAuthorize,
  // },

  // {
  //   path: "/about",
  //   name: "About",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/About.vue")
  // },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
