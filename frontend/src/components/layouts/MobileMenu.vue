<template>
    <div class='mobile-menu-core'>
        <!-- mobile menu topbar -->
       <div class='mobile-topbar hidden-md-and-up animated fadeInUp'>
           <v-icon medium color='white' class='ml-5' @click='$store.state.sidebarDrawer=true'>fas fa-bars</v-icon>
        </div>
       <!-- mobile menu -->
       <v-navigation-drawer 
            v-model="$store.state.sidebarDrawer" 
            color='#15141c' 
            fixed 
            top 
            width="65%" 
            height="100vh" 
            temporary 
            class="nav-drawer hidden-md-and-up pt-5"
        >
           <MenuContent/>
       </v-navigation-drawer>
    </div>
</template>

<script>
import MenuContent from "@/components/layouts/MenuContent.vue";
export default {
    name: 'MobileMenu',

    components: {
        MenuContent,
    },

    data(){
        return{
        }
    },

    created(){},

    methods: {}
}
</script>

<style scoped>
    .mobile-menu-core{
        width: 100%;
        height: 50px;
        display: flex;
        /* flex-direction: column; */
        justify-content: flex-start;
        align-items: center;
    }
    ::-webkit-scrollbar {
        width: 0px;
    }
    .mobile-topbar{
        width: 100%;
        height: 50px;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        position: fixed;
        top: 0px;
        z-index: 3;
        background-color: #15141c;
    }
    .nav-drawer {
        /* width: 100%; */
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        padding-left: 5px;
        /* top: 0px;
        z-index: 3; */
    }
    .v-navigation-drawer .v-navigation-drawer__content {
        width: 90%;
    }

</style>