<template>
    <div class='default-sidebar'>
        <div class='logo'>
            <div class='logo-img'></div>
            <h3 class='mt-3'>CHICAM</h3>
            <div class='warehouses-container mt-5 ml-5' v-if="$session.get('su')">
                <select class="warehouse-select" v-model='warehouse' @change='changeWarehouse()'>
                    <option value='all,0'>All</option>
                    <option v-for='(whouse, i) in warehouses[0]' :key='i' :value="whouse.name+','+whouse.id">{{whouse.name | suWarehouseName(whouse.su, whouse.name) | capitalize(whouse.name)}}</option>
                </select>
                <v-icon small color='white' style='position:relative;right:20px;'>fas fa-angle-down</v-icon>
            </div>
        </div>
        <!-- calendar ctrl -->
        <div class='claendar-ctrl mt-5 ml-2 hidden-md-and-up' style='display:flex;justify-content:flex-end;align-items:center;width:97%;'>
            <v-btn
                class="font-weight-bold"
                large
                color="#1976d2"
                style='cursor:pointer;text-transform:capitalize'
                rounded
                @click='$store.state.calendarStatus = !$store.state.calendarStatus, $store.state.sidebarDrawer=false'
            >
                <v-icon left style='font-size:20px;' class='pl-2 pt-2 pb-2' color='white'>
                    fas fa-calendar-alt
                </v-icon>
                <span v-if='$store.state.calendarStatus' style='color:white;'>Hide Calendar</span>
                <span v-else style='color:white;'>Show Calendar</span>
            </v-btn>
        </div>

        <div class='menu-container'>
            <router-link to="/dashboard" style="text-decoration: none;" class='menu-item'>
                <span style='border: 2px solid #1976d2; height:25px;' class='mr-5 animated rubberBand' v-if='$route.name=="Dashboard"'></span>
                <v-icon color='white'>fas fa-tachometer-alt</v-icon>
                <p>Dashboard</p>
            </router-link>

            <div class='link-container' v-if="$session.get('su')">
                <router-link to="/warehouses" style="text-decoration: none;" class='menu-item'>
                    <span style='border: 2px solid #1976d2; height:25px;' class='mr-5 animated rubberBand' v-if='$route.name=="Warehouse"'></span>
                    <v-icon color='white'>fas fa-warehouse</v-icon>
                    <p>W.house</p>
                </router-link>
                <v-icon 
                    style='font-size:28px;position:relative;bottom:1px' 
                    color='#0163d1' class='add-icon' 
                    @click='$store.state.dashboard.warehouseDialog=true, $store.state.dashboard.formActionType="add", $store.state.sidebarDrawer=false'
                >fas fa-plus-square</v-icon>
            </div>

            <div class='link-container'>
                <router-link to="/orders" style="text-decoration: none;" class='menu-item'>
                    <span style='border: 2px solid #1976d2; height:25px;' class='mr-5 animated rubberBand' v-if='$route.name=="Order"'></span>
                    <v-icon color='white'>fas fa-truck-loading</v-icon>
                    <p>Sales</p>
                </router-link>
                <v-icon 
                    style='font-size:28px;position:relative;bottom:1px' 
                    color='#0163d1' class='add-icon' 
                    @click='newOrder(), $store.state.sidebarDrawer=false'
                >fas fa-plus-square</v-icon>
            </div>

            <div class='link-container'>
                <router-link to="/products" style="text-decoration: none;" class='menu-item'>
                    <span style='border: 2px solid #1976d2; height:25px;' class='mr-5 animated rubberBand' v-if='$route.name=="Product"'></span>
                    <v-icon color='white'>fas fa-boxes</v-icon>
                    <p>Products</p>
                </router-link>
                <v-icon 
                    style='font-size:28px;position:relative;bottom:1px' 
                    color='#0163d1'
                    class='add-icon'
                    @click='addProduct(), $store.state.sidebarDrawer=false'
                >fas fa-plus-square</v-icon>
            </div>

            <div class='link-container'>
                <router-link to="/expenses" style="text-decoration: none;" class='menu-item'>
                    <span style='border: 2px solid #1976d2; height:25px;' class='mr-5 animated rubberBand' v-if='$route.name=="Expenses"'></span>
                    <v-icon color='white'>fas fa-wallet</v-icon>
                    <p>Expenses</p>
                </router-link>
                <v-icon 
                    style='font-size:28px;position:relative;bottom:1px' 
                    color='#0163d1'
                    class='add-icon'
                    @click='addExpenses(), $store.state.sidebarDrawer=false'
                >fas fa-plus-square</v-icon>
            </div>
            <div class='link-container' @click='newProforma()'>
                <p style='color:white;font-weight:bold;font-size:15px'>Proforma</p>
            </div>

            <!-- <div class='menu-item' v-if="!$route.name.startsWith('Dashboard')">
                <v-icon color='white'>fas fa-sort-amount-down-alt</v-icon>
                <p>Filters</p>
            </div> -->
        </div>

        <div class='setting-logout'>
            <router-link to="/settings" style="text-decoration: none;" class='settings'>
                <span style='border: 2px solid #1976d2; height:25px;' class='mr-5 animated rubberBand' v-if='$route.name=="Settings"'></span>
                <v-icon color='white'>fas fa-sliders-h</v-icon>
                <p>Settings</p>
            </router-link>

            <div @click='logout(), $store.state.sidebarDrawer=false' style="text-decoration: none;" class='logout'>
                <v-icon color='white'>fas fa-sign-out-alt</v-icon>
                <p>Log out</p>
            </div>
        </div>
            <!-- add new warehouse/user dialog -->
        <v-dialog
            v-model="$store.state.dashboard.warehouseDialog"
            persistent
            max-width="600px"
        >
            <v-form class='warehouse-form' ref='warehouseForm'>
                <h2 class='mb-5' v-if='$store.state.dashboard.formActionType=="add"'>Add new Warehouse</h2>
                <h2 class='mb-5' v-else>Update Warehouse</h2>
                <p class='err-msg mb-2'></p>
                <v-text-field
                    v-model="$store.state.dashboard.warehouseName"
                    :rules="[$store.state.rules.required]"
                    label="Warehouse name (will use as username)*"
                    required
                    outlined
                ></v-text-field>

                <v-text-field
                    v-model="$store.state.dashboard.email"
                    :rules="[$store.state.emailRules]"
                    label="Email"
                    outlined
                ></v-text-field>

                <v-text-field
                    v-if='$store.state.dashboard.formActionType=="add"'
                    v-model="$store.state.dashboard.upassword"
                    :rules="[$store.state.rules.required]"
                    label="Password*"
                    type='password'
                    required
                    outlined
                ></v-text-field>
                <v-text-field
                    v-if='$store.state.dashboard.formActionType=="update"'
                    v-model="$store.state.dashboard.upassword"
                    label="Password"
                    type='password'
                    outlined
                ></v-text-field>
                <v-text-field
                    v-if='$store.state.dashboard.formActionType=="add"'
                    v-model="$store.state.dashboard.rPassword"
                    :rules="[$store.state.rules.required]"
                    label="Repeat password*"
                    type='password'
                    required
                    outlined
                ></v-text-field>

                <div class='btn-container'>
                    <v-btn large @click='$store.state.dashboard.warehouseDialog=false' color='#1976d2' class='mr-3'>close</v-btn>
                    <v-btn large @click='addWarehouse()' color='#1976d2' v-if='$store.state.dashboard.formActionType=="add"'>Add Warehouse</v-btn>
                    <v-btn large @click='updateWarehouse($store.state.dashboard.warehouseId)' color='#1976d2' v-else>Update Warehouse</v-btn>
                </div>
            </v-form>
        </v-dialog>
    </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
    name: 'Sidebar',
    computed: {
        ...mapGetters({
            warehouses: 'dashboard/getWarehouse',
        }),
       
    },
    filters: {
        suWarehouseName: function(name, su){
            if(!su) return name
            name = 'main'
            return name
        }, 
        capitalize: function (value) {
            if (!value) return ''
            value = value.toString()
            return value.charAt(0).toUpperCase() + value.slice(1)
        }
    },
    data(){
        return{
            warehouse: this.$session.get('warehouseName'), //selected warehouse name
        }
    },
    created(){
        let self = this
        this.getWarehouses()
        setTimeout(() => {
            self.warehouse = this.$session.get('warehouseName')+','+this.$session.get('warehouseId')
        }, 100)
    },
    methods:{
         // product methods
        // allProducts(){
        //     let self = this;
        //     let store = self.$store;
        //     this.$store.dispatch("getReq", {
        //         url: "product/products",
        //         params: {
        //             date: null,
        //             user_id: this.$session.get('warehouseId')
        //         },
        //         auth: self.$session.get('token'),
        //         csrftoken: self.$session.get('token'),
        //         callback: function(data) {
        //             // console.log(data);
        //             store.getters["setData"]([store.state.product.productsArr, [data]]);
        //         },
        //     });
        // },
        changeWarehouse(){
            let self = this
            // update warehouse local session var
            this.$session.set('warehouseName', self.warehouse.split(',')[0])
            this.$session.set('warehouseId', self.warehouse.split(',')[1])
            window.location.reload()
        },
        addWarehouse(){
            let self = this
            let formErrMsg = document.querySelector(".err-msg");
            let validationErrMsg = document.querySelector('.v-messages__message');
            if(self.$store.state.dashboard.warehouseName != null &&
                self.$store.state.dashboard.upassword != null &&
                self.$store.state.dashboard.rPassword != null &&
                !document.body.contains(validationErrMsg)
            ){
                if(self.$store.state.dashboard.upassword == self.$store.state.dashboard.rPassword){
                    let body = {
                        username: self.$store.state.dashboard.warehouseName,
                        email: self.$store.state.dashboard.email,
                        password: self.$store.state.dashboard.upassword
                    }
                    self.$store.dispatch("postReq", {
                        url: 'dashboard/new_warehouse',
                        params: body,
                        auth: self.$session.get('token'),
                        csrftoken: self.$session.get('token'),
                        callback: function(data) {
                            // console.log(data);
                            if(data.created){
                                // self.$store.getters["setData"]([self.$store.state.dashboard.warehouseArr, [data]]);
                                formErrMsg.innerHTML = data.msg
                                document.querySelector('.warehouse-form').reset()
                                self.getWarehouses()
                                //close dialog after 2sec
                                setTimeout(() => {
                                    self.$store.state.dashboard.warehouseDialog = false
                                    formErrMsg.innerHTML = ''
                                }, 2000)
                            }else{
                                formErrMsg.innerHTML = data.msg
                            }
                        },
                    });
                }else{
                    formErrMsg.innerHTML = 'Passwords don t match'
                }
            }else{
                formErrMsg.innerHTML = 'warehouse name and password should not be empty'
            }
        },
        getWarehouses(){
            let self = this;
            self.$store.dispatch("getReq", {
                url: 'dashboard/get_warehouses',
                params: {},
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    // console.log(data);
                    self.$store.getters["setData"]([self.$store.state.dashboard.warehouseArr, [data]]);
                },
            });
        },
        whouseDetails(whouseId){
            let self = this;
            self.$store.dispatch("getReq", {
                url: 'dashboard/get_user_data',
                params: {user_id: whouseId},
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    console.log(data);
                    self.$store.getters["setData"]([self.$store.state.dashboard.whouseDetailsArr, [data]]);
                    self.$store.state.infoTempName = 'WhouseDetails'
                },
            });
        },
        updateWarehouse(whouseId){
            let self = this
            let formErrMsg = document.querySelector(".err-msg");
            let validationErrMsg = document.querySelector('.v-messages__message');
            // update warehouse
            if(self.$store.state.dashboard.warehouseName != '' ||
                self.$store.state.dashboard.email != ''||
                self.$store.state.dashboard.upassword != '' &&
                !document.body.contains(validationErrMsg)
            ){
                // send request
                self.$store.dispatch("putReq", {
                    url: 'dashboard/update_warehouse',
                    params: {
                        username: self.$store.state.dashboard.warehouseName,
                        email: self.$store.state.dashboard.email,
                        password: self.$store.state.dashboard.upassword,
                        id: whouseId
                    },
                    auth: self.$session.get('token'),
                    csrftoken: self.$session.get('token'),
                    callback: function(data) {
                        console.log(data);
                        if(data.updated){
                            formErrMsg.innerHTML = data.msg
                            document.querySelector('.warehouse-form').reset()
                            self.getWarehouses()
                            //close dialog after 2sec
                            setTimeout(() => {
                                self.$store.state.dashboard.warehouseDialog = false
                                formErrMsg.innerHTML = ''
                            }, 2000)
                        }else{
                            formErrMsg.innerHTML = data.msg
                        }
                    },
                });
            }else{
                formErrMsg.innerHTML = 'warehouse name or password or email should not be empty'
            }
        },
        logout(){
            let self = this;
            this.$store.dispatch("getReq", {
                url: "dashboard/signout",
                params: {
                },
                auth: self.$session.get('token'),
                csrftoken: self.$session.get('token'),
                callback: function(data) {
                    if(data.logout){
                        self.$session.destroy();
                        self.$router.push({name: 'Login'})
                    }
                },
            });
        },
        newOrder(){
            this.$store.state.formsDialog = true;
            this.$store.state.formName = 'Sale';
            this.$store.state.formsTemp = 'OrderStepper';
        },
        addProduct(){
            this.$store.state.formsDialog = true;
            this.$store.state.product.addProductForm = true;
            this.$store.state.product.productProforma = false;
            this.$store.state.formName = ' Product';
            this.$store.state.formsTemp = 'ProductForm';
            this.$store.reload = true;
        },
         newProforma(){
            this.$store.state.formsDialog = true;
            this.$store.state.formName = ' Proforma';
            this.$store.state.formsTemp = 'ProductForm';
            this.$store.state.product.addProductForm = false;
            this.$store.state.product.productProforma = true;
        },
        addExpenses(){
            this.$store.state.expenses.expensesDialog = true
        }
    }
}
</script>

<style scoped>
    .default-sidebar{
        height: 100%;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: flex-start;
        background-color: #15141c;
    }
    .logo{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        /* box-shadow: rgba(255, 255, 255, 0.2) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0.9) 0px 0px 0px 1px; */
    }
    .logo .logo-img{
        border: 1px solid #15141c;
        border-radius: 15px;
        background-image: url('../../assets/chicam.jpg');
        background-repeat: no-repeat;
        background-position: center;
        background-size: cover;
        width: 100px;
        height: 100px;
        border: 1px solid white;
        background-color: white;
    }
    .logo h3{
        text-align: center;
        color: white;
    }
    .warehouses-container{
        width: 90%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }
    .warehouse-select{
        width: 100%;
        height: 40px;
        border: 1px solid white;
        border-radius: 5px;
        color: white;
        padding-left: 10px;
        background-color: #15141c;
    }
    .menu-container{
        height: auto;
        width: 85%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-left: 15%;
    }
    .menu-item{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
        cursor: pointer;
        margin-bottom: 10px;
    }
    .link-container .menu-item{
        width: 50%;
    }
    .link-container{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
        cursor: pointer;
        margin-bottom: 10px;
    }
    .menu-item p,  .setting-logout p{
        color: white;
        font-weight: bold;
        font-size: 15px;
        margin-left: 10px;
        text-align: left;
        width: 70%;
    }
    .add-icon{
        margin-left: 30px;
    }
    .menu-item .v-icon, .setting-logout .v-icon{
        font-size: 18px;
    }
    .setting-logout{
        height: auto;
        width: 85%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-left: 15%;
    }
    .settings, .logout{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
        cursor: pointer;
    }
    /* dialog styles */
    .warehouse-form{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: white;
        padding-top: 50px;
        padding-bottom: 50px;
    }
    .err-msg{
        text-align: center;
        font-size: 17px;
        color: #ce2b58;
    }
    .warehouse-form .v-text-field{
        width: 85%;
    }
    .btn-container{
        height: auto;
        width: 85%;
        display: flex;
        flex-direction: row;
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
    @media only screen and (max-width: 1500px) {
        /* .sidebar-core{
            width: 20%;
        } */
        .add-icon{
            margin-left: 40px;
        }
    }
    @media only screen and (max-width: 500px) {
        .warehouses-container{
            width: 100%;
        }
        .warehouse-select{
        }
    }
</style>