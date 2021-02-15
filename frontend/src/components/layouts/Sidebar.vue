<template>
    <div class='sidebar-core'>
        <div class='logo'>
            <div></div>
            <h3 class='mt-3'>CHICAM</h3>
        </div>

        <div class='menu-container'>
            <router-link to="/dashboard" style="text-decoration: none;" class='menu-item'>
                <span style='border: 2px solid #1976d2; height:25px;' class='mr-5 animated rubberBand' v-if='$route.name=="Dashboard"'></span>
                <v-icon color='white'>fas fa-tachometer-alt</v-icon>
                <p>Dashboard</p>
            </router-link>

            <div class='link-container'>
                <router-link to="/orders" style="text-decoration: none;" class='menu-item'>
                    <span style='border: 2px solid #1976d2; height:25px;' class='mr-5 animated rubberBand' v-if='$route.name=="Order"'></span>
                    <v-icon color='white'>fas fa-truck-loading</v-icon>
                    <p>Orders</p>
                </router-link>
                <v-icon 
                    style='font-size:28px;position:relative;bottom:1px' 
                    color='#0163d1' class='add-icon' 
                    @click='newOrder()'
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
                    @click='addProduct()'
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
                    @click='addExpenses()'
                >fas fa-plus-square</v-icon>
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

            <div @click='logout()' style="text-decoration: none;" class='logout'>
                <v-icon color='white'>fas fa-sign-out-alt</v-icon>
                <p>Log out</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Sidebar',

    data(){
        return{

        }
    },

    created(){console.log(this.$route);},

    methods:{
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
            this.$store.state.formName = 'Order';
            this.$store.state.formsTemp = 'OrderStepper';
        },

        addProduct(){
            this.$store.state.formsDialog = true;
            this.$store.state.product.addProductForm = true;
            this.$store.state.formName = ' Product';
            this.$store.state.formsTemp = 'ProductForm';
            this.$store.reload = true;
        },

        addExpenses(){
            this.$store.state.expenses.expensesDialog = true
        }
    }
}
</script>

<style scoped>
    .sidebar-core{
        height: 100vh;
        width: 15%;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: flex-start;
        background-color: #15141c;
        position: fixed;
        top: 0px;
        left: 0px;
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
    .logo div{
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
    @media only screen and (max-width: 1500px) {
        /* .sidebar-core{
            width: 20%;
        } */
        .add-icon{
            margin-left: 40px;
        }
    }
</style>