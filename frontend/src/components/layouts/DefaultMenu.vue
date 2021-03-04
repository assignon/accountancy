<template>
    <div class='sidebar-core'>
       <MenuContent/>
    </div>
</template>

<script>
import MenuContent from "@/components/layouts/MenuContent.vue";
export default {
    name: 'DefaultMenu',

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
     .sidebar-core{
        height: 100vh;
        width: 15%;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: flex-start;
        position: fixed;
        top: 0px;
        left: 0px;
        background-color: #15141c;
    }
</style>