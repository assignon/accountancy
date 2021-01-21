<template>
  <div class="login-core">
    <v-layout class='login-layout'>
      <h2>Signin</h2>
      <v-form class='login-form' ref='loginForm'>
        <p class='err-msg'></p>
        <v-text-field
            v-model="email"
            :rules="[$store.state.emailRules, $store.state.rules.required]"
            label="Email"
            type='email'
            required
            outlined
        ></v-text-field>

        <v-text-field
            v-model="password"
            :rules="[$store.state.rules.required]"
            label="Password"
            type='password'
            required
            outlined
        ></v-text-field>
        <div class='btn-container'>
          <v-btn medium @click='signin()'>Login</v-btn>
          <p>password forgot?</p>
        </div>
      </v-form>
    </v-layout>
  </div>
</template>

<script>
// import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "Home",
  components: {
  },

  data(){
    return{
      email: null,
      password: null,
    }
  },

  created(){
    
  },

  methods: {
    startSession(token, userId){
      // start a session
      this.$session.start()
      // store token en user id
      this.$session.set('token', token)
      this.$session.set('userId', userId)
      this.$session.set('authenticated', true)
    },

    signin(){
      let self = this;
      let formErrMsg = document.querySelector('.err-msg')
      let validationErrMsg = document.querySelector('.v-messages__message');

      if(!document.body.contains(validationErrMsg) && self.email != null && self.password != null){
        this.$store.dispatch("postReq", {
          url: "signin",
          params: {
              email: self.email,
              password: self.password
          },
          auth: null,
          csrftoken: null,
          callback: function(data) {
              console.log(data);
              if(data.authenticate){
                self.startSession(data.token, data.user_id)
                self.$router.push({name: "Dashboard"})
              }else{
                 formErrMsg.innerHTML = data.msg
              }
          },
        });
      }else{
          formErrMsg.innerHTML = 'Email and password should not be empty';
      }

    }
  }
};
</script>

<style scoped>
  
</style>
