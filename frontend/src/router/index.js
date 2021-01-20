import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";
// import Dashboard from "../views/dashboard/Dashboard.vue";
// import NotAuthorize from "../views/dashboard/NotAuthorize.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login,
  },
  // {
  //   path: "/dashboard",
  //   name: "Dashboard",
  //   component: Home
  // },
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
