<template>
    <div class='sidebar-core'>
        <div class='logo'>
            <v-img></v-img>
            <h3 class='mt-3'>CHICAM</h3>
        </div>

        <div class='menu-container'>
            <router-link to="/dashboard" style="text-decoration: none;" class='menu-item'>
                <v-icon color='white'>fas fa-tachometer-alt</v-icon>
                <p>Dashboard</p>
            </router-link>

            <div class='link-container'>
                <router-link to="/orders" style="text-decoration: none;" class='menu-item'>
                    <v-icon color='white'>fas fa-truck-loading</v-icon>
                    <p>Orders</p>
                </router-link>
                <v-icon 
                    style='font-size:28px;position:relative;bottom:1px' 
                    color='#0163d1' class='ml-3' 
                    @click='newOrder()'
                >fas fa-plus-square</v-icon>
            </div>

            <div class='link-container'>
                <router-link to="/products" style="text-decoration: none;" class='menu-item'>
                    <v-icon color='white'>fas fa-boxes</v-icon>
                    <p>Products</p>
                </router-link>
                <v-icon style='font-size:28px;position:relative;bottom:1px' color='#0163d1' class='ml-3'>fas fa-plus-square</v-icon>
            </div>

            <div class='menu-item' v-if="!$route.name.startsWith('Dashboard')">
                <v-icon color='white'>fas fa-sort-amount-down-alt</v-icon>
                <p>Filters</p>
            </div>
        </div>

        <div class='setting-logout'>
            <router-link to="/settings" style="text-decoration: none;" class='settings'>
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

    created(){},

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
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .logo .v-image{
        width: 70PX;
        height: 70px;
        border: 1px solid white;
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
</style>