<template>
  <v-app id='app'>
    <v-main>
      <DefaultMenu v-if="!$route.name.startsWith('Login')" class='hidden-sm-and-down' />
      <MobileMenu v-if="!$route.name.startsWith('Login')" class='hidden-md-and-up' />
      <router-view class="animated fadeIn"></router-view>
      <FormsModal/>
      <v-dialog
        v-model="$store.state.pdfDialog"
        fullscreen
        hide-overlay
        transition="dialog-bottom-transition"
        class='pdf-dialog'
      >
        <!-- <OrderPdf /> -->
        <component :is="$store.state.pdfTemp"></component>
      </v-dialog>
      <!-- expenses dialog -->
      <v-dialog
            v-model="$store.state.expenses.expensesDialog"
            persistent
            max-width="600px"
        >
            <ExpensesForm />
        </v-dialog>
    </v-main>
  </v-app>
</template>

<script>
import DefaultMenu from "./components/layouts/DefaultMenu";
import MobileMenu from "./components/layouts/MobileMenu";
import FormsModal from "./components/modals/FormsModal";
import OrderPdf from "@/components/layouts/OrderPdf.vue";
import ProductPdf from "@/components/layouts/ProductPdf.vue";
import ExpensesForm from "@/components/layouts/forms/ExpensesForm.vue";
import ProformaPdf from "@/components/layouts/ProformaPdf.vue";

export default {
  name: "App",

  components: {
    DefaultMenu,
    MobileMenu,
    FormsModal,
    OrderPdf, 
    ProductPdf,
    ExpensesForm,
    ProformaPdf,
  },

  data: () => ({
    //
  }),

  created(){
    setInterval(() => {
      let link = document.createElement('a')
      link.href = '/backup'
      link.click()
    }, 604800000)
  },

  methods: {
    makeBackup(){
      let self = this

      this.$store.dispatch("getReq", {
          url: "dashboard/db_backup",
          params: {},
          auth: self.$session.get('token'),
          csrftoken: self.$session.get('token'),
          callback: function(data) {
              console.log(data);
          },
      });
    },

    createSession() {
      if (!this.$session.has("auth")) {
        this.$session.start();
        this.$session.set("auth", false);
      }
      this.$store.state.AUTHENTICATED = this.$session.get("auth");
      // console.log(this.$store.state.AUTHENTICATED);
    },
  }
};
</script>

<style scoped>
html,
body {
  scroll-behavior: smooth;
  overflow-x: hidden;
  width: 100%;
  margin: 0px;
  padding: 0px;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0px;
  padding: 0px;
  width: 100%;
  height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
