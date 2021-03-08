<template>
    <div class='settings-core'>
        <div class='user-data'>
            <div class='user-logo'></div>
            <v-form class='user-data-form' ref='userDataForm'>
                <p class='form-err-msg'></p>
                <v-text-field
                    v-model="email"
                    :rules="[$store.state.rules.required]"
                    label="Email*"
                    type="email"
                    required
                    outlined
                ></v-text-field>
                <v-text-field
                    v-model="name"
                    :rules="[$store.state.rules.required]"
                    label="Name*"
                    required
                    outlined
                ></v-text-field>
                <p>Change Password</p>
                <v-text-field
                    v-model="password"
                    label="Password*"
                    type="password"
                    required
                    outlined
                ></v-text-field>
                <!-- <v-text-field
                    v-model="repeatPassword"
                    label="Repeat Password*"
                    type="password"
                    required
                    outlined
                ></v-text-field> -->
                <p>Confirm the changes</p>

                <div class="btn-container">
                    <v-flex xs12 sm12 md9 lg9 xl9>
                        <v-text-field
                            v-model="currentPassword"
                            :rules="[$store.state.rules.required]"
                            label="Current Password*"
                            type="password"
                            required
                            outlined
                        ></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm12 md3 lg3 xl3 class='btn-flex'>
                        <v-btn
                            depressed
                            height="50"
                            :width="btnWidth"
                            class="fot-weight-bold white--text mr-2"
                            color="#1976d2"
                            @click="updateUserData()"
                        >
                            <p style='font-size:17px;margin:auto;color:white;'>Update</p>
                        </v-btn>
                    </v-flex>
                </div>
                <p class='form-msg'></p>
            </v-form>
            <!-- backup settings -->
            <div class='backup'>
                <h1 class='mt-5 mb-3' style='color: #1976d2'>DataBase Backups</h1>
                <p> Backups are made on a weekly bases and it's stored in a local <strong>Downloads</strong> folder.</p>
                <v-btn
                    depressed
                    height="50"
                    large
                    class="fot-weight-bold white--text mt-5"
                    color="#1976d2"
                >
                    <v-icon medium color='white'>fas fa-download</v-icon>
                    <a href="/backup" style='font-size:17px;margin:auto;color:white;' class='ml-1 font-weight-bold'>Backup Manually</a>
                </v-btn>
                <!-- <a v-if='sqlite3!=null' href='../../../db.sqlite3' download >DB</a> -->
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    name: 'UserDate',

    computed: {
         ...mapGetters({
            userData: 'dashboard/getUserData',
        }),
    },

    data(){
        return{
            email: null,
            name: null,
            password: null,
            currentPassword: null,
            repeatPassword: null,
            btnWidth: window.innerWidth > 500 ? '70%' : '100%',
            sqlite3: null
        }
    },

    created(){
        this.getUserData(this.$session.get('userId'))
        this.$store.state.infoDrawer = false
    },

    methods: {
        // makeBackup(){
        //     let self = this

        //     this.$store.dispatch("getReq", {
        //         url: "dashboard/db_backup",
        //         params: {},
        //         auth: self.$session.get('token'),
        //         csrftoken: self.$session.get('token'),
        //         callback: function(data) {
        //             console.log(data);
        //             // let headers = data.headers();
        //             let blob = new Blob([data], { type: 'application/x-sqlite3' })
        //             // url = window.URL.createObjectURL(blob)

        //             let link = document.createElement('a')
        //             link.href = window.URL.createObjectURL(blob)
        //             link.download = 'db.sqlite3'
        //             link.click()

        //             // window.open(url)
        //         },
        //     });
        // },

        getUserData(userId){
            let self = this

            this.$store.dispatch("getReq", {
                url: "dashboard/get_user_data",
                params: {
                    user_id: userId
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log(data);
                    self.email = data.email
                    self.name = data.name
                    self.$store.getters["setData"]([self.$store.state.dashboard.userDataArr, [data]]);
                },
            });
        },

        updateUserData(){
            let self = this;
            let formErrMsg = document.querySelector(".form-msg");
            let validationErrMsg = document.querySelector('.v-messages__message');

            if (self.email != null && self.name != null &&  self.currentPassword !== null) {
                if(!document.body.contains(validationErrMsg)){
                    // if(self.password != null || self.repeatPassword != null){
                    //     if(self.password != self.repeatPassword){
                    //         formErrMsg.innerHTML = "The passwords are not equals"
                    //         return false
                    //     }
                    // }
                    this.$store.dispatch("putReq", {
                        url: "dashboard/update_user_data",
                        params: {
                            user_id: self.$session.get('userId'),
                            email: self.email,
                            name: self.name,
                            current_password: self.currentPassword,
                            password: self.password != null ? self.password : null,
                        },
                        auth: self.$session.get('token'),
                        csrftoken: self.$session.get('token'),
                        callback: function(data) {
                            // console.log(data);
                            if(data.updated){
                                self.getUserData(data.user_id)
                                formErrMsg.innerHTML = data.msg
                                alert('User data updated')
                                setTimeout(() => {
                                    formErrMsg.innerHTML = ''
                                })
                            }else{
                                formErrMsg.innerHTML = data.msg
                            }
                        },
                    });
                }else{
                    formErrMsg.innerHTML = validationErrMsg.textContent;
                }
            } else {
                formErrMsg.innerHTML = "Fields are empty";
            }
        }
    }
}
</script>

<style scoped>
    .settings-core{
        height: auto;
        width: 85%;
        display: flex;
        justify-content: center;
        align-items: flex-start;
        margin-left: 15%;
        margin-top: 70px;
        background-color: #fff;
    }
    .user-logo{
        width: 200px;
        height: 200px;
        margin-bottom: 30px;
        border-radius: 15px;
        border: 1px solid #15141c;
        border-radius: 15px;
        background-image: url('../assets/chicam.jpg');
        background-repeat: no-repeat;
        background-position: center;
        background-size: cover;
        box-shadow: rgba(255, 255, 255, 0.2) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0.9) 0px 0px 0px 1px;
    }
    .user-data{
        width: 70%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .user-data-form{
        width: 70%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .user-data-form p{
        font-size: 17px;
        font-weight: bold;
        color: #15141c;
    }
    .form-err-msg{
        width: 100%;
        height: auto;
        text-align: left;
        color: #15141c;
        font-size: 15px;
    }
     .user-data-form .v-text-field{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        /* margin-bottom: 20px;
        margin-top: 20px; */
    }
    .btn-container{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        align-items: flex-start;
    }
    .v-btn{
        text-transform: capitalize;
        color: white;
    }
    .backup{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        margin-bottom: 70px;
    }
    .backup p{
        padding: 0px;
        margin: 0px;
    }
    @media only screen and (max-width: 500px){
         .settings-core{
            width: 95%;
            align-items: center;
            margin-left: 5%;
            margin-top: 30px;
        }
        .user-data{
            width: 100%;
        }
        .user-data-form{
            width: 90%;
        }
        .btn-container{
            flex-direction: column;
            justify-content: flex-start;
            margin-bottom: 20px;
        }
        .btn-container .v-text-field{
            width: 100%;
        }
    }
</style>