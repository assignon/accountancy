<template>
  <div class="login-core animated fadeIn">
      <div class='logo mb-5'></div>
      <h2 class='mb-3'>CHIICAM Signin</h2>
      <v-form class='login-form' ref='loginForm'>
        <p class='err-msg mb-2'></p>
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
          <v-btn large @click='signin()' color='#1976d2'>Login</v-btn>
          <p class='mt-2' @click='$store.state.passForgotDialog=true'>password forgot?</p>
        </div>
      </v-form>
      <PasswordForgot/>
  </div>
</template>

<script>
import PasswordForgot from "@/components/modals/PasswordForgot.vue";

export default {
  name: "Home",
  components: {
    PasswordForgot,
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
        this.$store.dispatch("publicPostReq", {
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
                self.startSession(data.token, data.id)
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
  .login-core{
    height: 100vh;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .logo{
    width: 100px;
    height: 100px;
    border: 1px solid #15141c;
  }
  .login-core h2{
    text-align: center;
  }
  .login-form{
    height: auto;
    width: 35%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .err-msg{
    text-align: center;
    font-size: 17px;
    color: #ce2b58;
  }
  .login-form .v-text-field{
    width: 100%;
  }
  .btn-container{
    height: auto;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: flex-end;
  }
  .btn-container .v-btn{
    color: #fff;
    font-size: 15px;
    font-weight: bolder;
    text-transform: capitalize;
  }
  .btn-container p{
    text-align: right;
    font-size: 17px;
    font-weight: bolder;
    cursor: pointer;
    color: #1976d2;
  }
</style>
