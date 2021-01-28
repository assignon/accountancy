<template>
    <v-dialog
      v-model="$store.state.passForgotDialog"
      transition="dialog-bottom-transition"
      width="550"
      hide-overlay
    >
      <v-form class='password-forgot-form'>
        <div class='header'>
            <h4>Reset your password</h4>
        </div>
        <p class='forgot-err-msg mb-2'></p>
        <v-text-field
            v-model="$store.state.forgotEmail"
            :rules="[$store.state.emailRules, $store.state.rules.required]"
            label="Email"
            type='email'
            required
            outlined
        ></v-text-field>
        <div class='btn-container'>
          <v-btn large @click='sendNewPassword()' color='#1976d2'>Reset Password</v-btn>
        </div>
      </v-form>
    </v-dialog>
</template>

<script>
export default {
    name: 'PasswordForgot',

    data(){
        return{
        }
    },

    methods: {
        sendNewPassword(){}
    }
}
</script>

<style scoped>
   /* .v-dialog{
      display: flex;
      justify-content: center;
      align-items: center;
   } */
  .password-forgot-form{
    height: auto;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding:70px 50px 70px 50px;
    background-color: #f5f6f8; 
    border: 1px solid #f5f6f8;
  }
  .header{
    height: auto;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    margin-bottom: 20px;
  }
  .forgot-err-msg{
    text-align: center;
    font-size: 17px;
    color: #ce2b58;
  }
  .password-forgot-form .v-text-field{
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
 
</style>