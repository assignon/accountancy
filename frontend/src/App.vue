<template>
  <v-app id='app'>
    <v-main>
      <Sidebar v-if="!$route.name.startsWith('Login')" />
      <router-view class="animated fadeIn"></router-view>
      <FormsModal/>
      <v-dialog
        v-model="$store.state.pdfDialog"
        fullscreen
        hide-overlay
        transition="dialog-bottom-transition"
        class='pdf-dialog'
      >
        <OrderPdf />
    </v-dialog>
    </v-main>
  </v-app>
</template>

<script>
import Sidebar from "./components/layouts/Sidebar";
import FormsModal from "./components/modals/FormsModal";
import OrderPdf from "@/components/layouts/OrderPdf.vue";

export default {
  name: "App",

  components: {
    Sidebar,
    FormsModal,
    OrderPdf
  },

  data: () => ({
    //
  }),

  created(){},

  methods: {
    createSession() {
      if (!this.$session.has("auth")) {
        this.$session.start();
        this.$session.set("auth", false);
      }
      this.$store.state.AUTHENTICATED = this.$session.get("auth");
      console.log(this.$store.state.AUTHENTICATED);
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
